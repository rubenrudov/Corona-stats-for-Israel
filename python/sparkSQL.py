# TODO: combine with load_json, add crawler (input) & firebase (output) & scheduler (batch timing)
import json
import logging
import time
import winsound
from typing import Any, Union, List, Dict

from pyspark import RDD
from pyspark.sql import Row
from pyspark.python.pyspark.shell import spark
from pyspark.sql import SparkSession, DataFrame, Column

from Spark.Spark_handler_class import Spark_handler


def to_spark():
    st = time.time()



    # json_count_names: dict = Spark_handler.pass_to_spark(
    #     file_path=f"{HDFS_handler.DEFAULT_CLUSTER_PATH}{HDFS_handler.HADOOP_USER}/{CITY_JSON}",
    #     process_fn=process_data
    # )

    spark_session = SparkSession \
        .builder \
        .enableHiveSupport() \
        .getOrCreate()

    # print(spark_session.read.json("json/city_json.json"))
    df: DataFrame = spark_session.read.json("json/city_json.json")
    # df.printSchema()
    df.show()
    # cities: Column = df.result.records
    # cities: Column = df["result"]["records"]
    #
    # # df.select(df.result.records.getField("City_Name")).show()
    # df.select(cities.getField("City_Name")).show()
    # df.select(cities("City_Name")).show()
    df.createOrReplaceTempView("table_1")

    df2: DataFrame = spark.sql("SELECT result from table_1")
    # print(df2.collect())
    # df2.printSchema()
    # df2.createOrReplaceTempView("table_2")
    #
    # df3: DataFrame = spark.sql("SELECT result FROM table_2 WHERE result='records'")
    # df3.printSchema()
    # df3.show()
    # # print(df3.collect())
    # # print(df3.select("records"))
    # df3.createOrReplaceTempView("table_3")
    #
    # cities_records: DataFrame = spark.sql("SELECT * from table_3")
    # cities_records.printSchema()
    df2.show()
    # results: list = df2.collect()
    # res: Row = results.pop()
    # print(res)
    rdd: RDD = df2.toJSON()
    print(rdd.count())
    # print(type(rdd.first()))
    first_elem: str = rdd.first()
    # rdd.flatMapValues()
    print(first_elem[0:5000:1], len(first_elem))
    dict_root: dict = json.loads(first_elem)
    print()
    print(dict_root["result"].keys())
    print(dict_root["result"]["records"].pop())
    cities: List[Dict[str, str, str, str, str, str, str, str, str, int]] = dict_root["result"]["records"]
    citiesDF: DataFrame = spark.createDataFrame(data=cities)
    citiesDF.printSchema()
    citiesDF.show(truncate=False)
    from datetime import date
    today = date.today()
    print("Today's date:", today)
    print(type(citiesDF.filter(citiesDF.Date >= date.today())))
    filteresDF: DataFrame = citiesDF.filter(citiesDF.Date >= "2021-01-09")
    filteresDF.show()


    # from testsAndOthers.data_types_and_structures import DataTypesHandler, PrintForm
    # DataTypesHandler.print_data_recursively(data=json_count_names, print_dict=PrintForm.PRINT_DICT.value)

    logging.debug(f"spark total time: {time.time() - st} seconds")


def main():
    st = time.time()

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('flaskwebgui').setLevel(logging.ERROR)
    logging.getLogger('BaseHTTPRequestHandler').setLevel(logging.ERROR)
    logging.getLogger('matplotlib').setLevel(logging.ERROR)
    logging.getLogger('py4j').setLevel(logging.ERROR)
    logging.getLogger('my_log').setLevel(logging.DEBUG)

    try:
        to_spark()
    finally:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        logging.debug(f"Program Total Time: {time.time() - st} seconds")


if __name__ == '__main__':
    main()


# root
#  |-- help: string (nullable = true)
#  |-- result: struct (nullable = true)
#  |    |-- _links: struct (nullable = true)
#  |    |    |-- next: string (nullable = true)
#  |    |    |-- start: string (nullable = true)
#  |    |-- fields: array (nullable = true)
#  |    |    |-- element: struct (containsNull = true)
#  |    |    |    |-- id: string (nullable = true)
#  |    |    |    |-- type: string (nullable = true)
#  |    |-- include_total: boolean (nullable = true)
#  |    |-- limit: long (nullable = true)
#  |    |-- records: array (nullable = true)
#  |    |    |-- element: struct (containsNull = true)
#  |    |    |    |-- City_Code: string (nullable = true)
#  |    |    |    |-- City_Name: string (nullable = true)
#  |    |    |    |-- Cumulated_deaths: string (nullable = true)
#  |    |    |    |-- Cumulated_number_of_diagnostic_tests: string (nullable = true)
#  |    |    |    |-- Cumulated_number_of_tests: string (nullable = true)
#  |    |    |    |-- Cumulated_recovered: string (nullable = true)
#  |    |    |    |-- Cumulated_vaccinated: string (nullable = true)
#  |    |    |    |-- Cumulative_verified_cases: string (nullable = true)
#  |    |    |    |-- Date: string (nullable = true)
#  |    |    |    |-- _id: long (nullable = true)
#  |    |-- records_format: string (nullable = true)
#  |    |-- resource_id: string (nullable = true)
#  |-- success: boolean (nullable = true)
