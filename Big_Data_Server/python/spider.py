import json
import logging
import os
import time
import urllib.request
import winsound
from http.client import HTTPResponse
from typing import Dict, List, Any, Union

import requests
from pyspark import RDD
from pyspark.sql import DataFrame

from SQL.SQLite_database_handler import SQLite_handler

# URL_GOV = 'https://data.gov.il/api/3/action/datastore_search?resource_id=dcf999c1-d394-4b57-a5e0-9d014a62e046'
URL_GOV = 'https://data.gov.il/api/3/action/datastore_search?' \
          'resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&limit=1000000000'
CITY_JSON = "city_json.json"
TABLENAME = "City_Table"
SCHEMA = "_id INT, City_Name VARCHAR(255), City_Code INT, Date VARCHAR(255)," \
             " Cumulative_verified_cases INT, Cumulated_recovered INT, Cumulated_deaths INT," \
         " Cumulated_number_of_tests INT, Cumulated_number_of_diagnostic_tests INT, Cumulated_vaccinated INT"

# print(type(fileobj))
# print(fileobj.read())

# with urllib.request.urlopen(URL_GOV) as url:
#     s = url.read()
#     # I'm guessing this would output the html source code ?
#     print(s)


def save_json_to_hdfs(filename: str, file_path: str):
    from Hadoop.hdfs import HDFS_handler
    HDFS_handler.start()

    HDFS_handler.delete_file(filename=filename)
    HDFS_handler.create_file(file_path=file_path)
    time.sleep(2)
    HDFS_handler.list_files()

    HDFS_handler.stop()


def save_json_to_sqlite(json_file_path: str, schema: str, db_path: str, tablename: str):
    st = time.time()

    import json
    with open(json_file_path) as f:
        print(f.read())
        data = json.load(f)
    # print(type(data))

    SQLite_handler.exec_all(db_path, f"DROP TABLE {tablename};")
    SQLite_handler.create_table(db_path=db_path, table_schema=schema, tablename=tablename)
    SQLite_handler.insert_json(json=data, tablename=tablename, db_path=db_path)

    logging.debug(f"sqlite total time: {time.time() - st} seconds")


def process_data(data_frame: DataFrame) -> Dict:
    from pyspark import SparkContext
    import pyspark
    from Spark.Spark_handler_class import Spark_handler
    sc: SparkContext = Spark_handler.spark_context_setup(log_level="ERROR")

    pickle: list = data_frame.collect()  # Union[List[Any], Any] = list
    # logging.warning(type(pickle))
    # print(pickle)
    rdd: pyspark.rdd.RDD = sc.parallelize(pickle)  # Union[RDD, Any] = RDD
    # logging.warning(type(rdd))

    temp_dict = {}
    temp_list = []
    #     temp_dict: Accumulator = sc.accumulator(dict())
    objects_list: List[pyspark.Row] = rdd.collect()
    # print(objects_list)
    # from testsAndOthers.data_types_and_structures import DataTypesHandler
    # DataTypesHandler.print_data_recursively(objects_list)

    data = json.load(objects_list)
    print(data)

    # create values list (clean data)
    for row in objects_list:
        if row.value == "[" or row.value == "]": continue
        # print(row.asDict())
        # dict_str: str = pyspark.sql.types.Row.asDict(row, True)["value"].split(",")[0][1:]  # .split("{")[1]
        # print(dict_str)
        # dict_list = dict_str.split(":")
        # print(dict_list[0], dict_list[1][1:])
        # temp_dict[dict_list[0].split("\"")[1]] = dict_list[1][1:].split("\"")[1]  # .replace(" ", "_")
        # # temp_dict[dict_list[1][1:]] = temp_dict[dict_list[0]]
        #
        # # temp_list.append(dict_list[1][1:].split("\"")[1].split(" ")[0])  # first names
        # temp_list.append(dict_list[1][1:].split("\"")[1])  # author names
        # print(temp_list)
        # print(temp_dict)
        string = row.asDict()["value"]
        # print(string)
        data = json.load(string)
        print(data)
        time.sleep(3)
        return

        # for row2 in row.asDict().values():
        #     print(type(row2))
        #     import json
        #     data = json.loads(row2.encode())
        #     print(type(data))
        #     time.sleep(3)
        #     return

    # create key-value pairs
    sc.emptyRDD()
    reduced_rdd: RDD = sc.parallelize(temp_list)

    # filter (lambda list.pop : bool)
    from pyspark.rdd import PipelinedRDD
    filtered: PipelinedRDD = reduced_rdd.filter(lambda name: name)  # all names
    print("Fitered RDD -> %s" % filtered.collect())

    # map (lambda list.pop : key_value_tuple)
    # map (lambda old_element : new_element)
    mapped: PipelinedRDD = filtered.map(lambda x: (x, 0))
    print("Key value pair -> %s" % mapped.collect())
    logging.critical(dict(mapped.collect()))

    # count number of items (reduce)
    dictionary_vals: dict = dict(mapped.collect())  # without duplicates
    for item in mapped.collect():
        dictionary_vals[item[0]] += 1

    logging.critical(dictionary_vals)

    sc.emptyRDD()

    # SQLite_handler(db_path=r"C:\cyber\PortableApps\SQLiteDatabaseBrowserPortable\first_sqlite_db.db")
    # SQLite_handler.create_table(db_path=SQLite_handler.db_path, table_schema=SCHEMA, tablename=TABLENAME)
    # # SQLite_handler.exec_all(SQLite_handler.db_path, f"DROP TABLE {TABLENAME};")
    # SQLite_handler.insert_json(json=pickle, tablename=TABLENAME, db_path=SQLite_handler.db_path,
    #                            special_chars=False)
    # # SQLite_handler.exec_all(SQLite_handler.db_path, f"SELECT * FROM {TABLENAME};")

    return dictionary_vals


def to_spark():
    st = time.time()

    from Hadoop.hdfs import HDFS_handler
    from Spark.Spark_handler_class import Spark_handler

    HDFS_handler.start()
    HDFS_handler.safemode_off()

    json_count_names: dict = Spark_handler.pass_to_spark(
        file_path=f"{HDFS_handler.DEFAULT_CLUSTER_PATH}{HDFS_handler.HADOOP_USER}/{CITY_JSON}",
        process_fn=process_data
    )

    HDFS_handler.safemode_on()
    HDFS_handler.stop()

    from testsAndOthers.data_types_and_structures import DataTypesHandler, PrintForm
    DataTypesHandler.print_data_recursively(data=json_count_names, print_dict=PrintForm.PRINT_DICT.value)

    # # elastic
    # from BD_projects.moto_prices.moto_crawler import MotoCrawler
    # MotoCrawler.upload_json_to_elastic(json=json_count_names)

    # TODO: firebase
    # SQLite_handler(db_path=r"C:\cyber\PortableApps\SQLiteDatabaseBrowserPortable\first_sqlite_db.db")
    # #SQLite_handler.exec_all(SQLite_handler.db_path, f"DROP TABLE {TABLENAME};")
    # SQLite_handler.create_table(db_path=SQLite_handler.db_path, table_schema=SCHEMA, tablename=TABLENAME)
    # SQLite_handler.insert_json(json=json_count_names, tablename=TABLENAME, db_path=SQLite_handler.db_path,
    #                            special_chars=False)
    # #SQLite_handler.exec_all(SQLite_handler.db_path, f"SELECT * FROM {TABLENAME};")

    logging.debug(f"spark total time: {time.time() - st} seconds")


def main():
    logging.getLogger('flaskwebgui').setLevel(logging.ERROR)
    logging.getLogger('BaseHTTPRequestHandler').setLevel(logging.ERROR)
    logging.getLogger('matplotlib').setLevel(logging.ERROR)
    logging.getLogger('py4j').setLevel(logging.ERROR)
    logging.getLogger('my_log').setLevel(logging.DEBUG)

    def crawl_into_hdfs():
        # fileobj: HTTPResponse = urllib.request.urlopen(URL_GOV)
        fileobj: dict = requests.get(URL_GOV).json()

        try:
            os.mkdir(f"json/{CITY_JSON}")
        except FileExistsError:
            logging.debug("file exists")
        time.sleep(1)
        # with open(f"json/{CITY_JSON}", "w") as file:  # create the file
        #     file.write(str(fileobj.read()))
        #     # print(os.path.dirname(os.path.abspath(file.name)))
        #     # print(os.path.abspath(file.name))
        #     save_json_to_hdfs(filename=file.name, file_path=os.path.abspath(file.name))
        with open(f"json/{CITY_JSON}", 'w') as outfile:
            json.dump(fileobj, outfile)
            save_json_to_hdfs(filename=outfile.name, file_path=os.path.abspath(outfile.name))

    # crawl_into_hdfs()
    to_spark()

    SQLite_handler(db_path=r"C:\cyber\PortableApps\SQLiteDatabaseBrowserPortable\first_sqlite_db.db")
    #save_json_to_sqlite(json_file_path="json/city_json.json", schema=SCHEMA, tablename=TABLENAME, db_path=SQLite_handler.db_path)
    #SQLite_handler.exec_all(SQLite_handler.db_path, f"SELECT * FROM {TABLENAME};")

    # SQLite_handler.exec_all(SQLite_handler.db_path, f"SELECT * FROM {TABLENAME};")

    winsound.MessageBeep(winsound.MB_OK)


if __name__ == '__main__':
    main()
