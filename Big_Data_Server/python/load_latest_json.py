import datetime
import json
import logging
import time
import winsound
from typing import List, Dict, Any, Union

import requests as requests
from firebase import Firebase

from apscheduler.schedulers.blocking import BlockingScheduler
# https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# https://data.gov.il/dataset/covid-19  # מאגר קורונה
# https://data.gov.il/dataset/covid-19/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69  # טבלת יישובים
# https://data.gov.il/dataset/covid-19/resource/0995c344-6a7a-4557-99ff-28ee6f3149b3  # טבלת יישובים README
# https://data.gov.il/dataset/covid-19/resource/89f61e3a-4866-4bbf-bcc1-9734e5fee58e  # קבוצות מין וגיל
# https://console.firebase.google.com/u/2/project/corona-charts-33e8a/database/corona-charts-33e8a-default-rtdb/data/~2F
# https://stackoverflow.com/questions/30483977/python-get-yesterdays-date-as-a-string-in-yyyy-mm-dd-format/30484112
from pyspark import RDD, Row, Accumulator
from pyspark.python.pyspark.shell import spark
from pyspark.sql import SparkSession, DataFrame, Column
from pyspark.sql.functions import explode, create_map


class Constants:
    db = {}
    URL_GOV = 'https://data.gov.il/api/3/action/datastore_search?' \
              'resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&limit=100000000'
    SCHEDULER: BlockingScheduler = BlockingScheduler()
    # json_rows = []


def firebase_config():
    config = {
        # "apiKey": "apiKey",
        # "authDomain": "projectId.firebaseapp.com",
        # "databaseURL": "https://databaseName.firebaseio.com",
        # "storageBucket": "projectId.appspot.com",
        # "serviceAccount": "path/to/serviceAccountCredentials.json"  # (optional)

        "apiKey": "AIzaSyCOt619fNqEuIgFpzf20h2cmC6tFeQYuTE",
        "authDomain": "corona-charts-33e8a.firebaseapp.com",
        "databaseURL": "https://corona-charts-33e8a-default-rtdb.firebaseio.com/",
        "storageBucket": "corona-charts-33e8a.appspot.com"
    }

    firebase = Firebase(config)

    Constants.db = firebase.database()


def crawl_corona():
    response: dict = requests.get(Constants.URL_GOV).json()
    # print(response["result"]["records"].pop().items())
    # return
    to_spark_direct_upside_down(cities=response["result"]["records"])
    # my_dict2 = {y: x for x, y in filteresDF.toPandas().to_dict().items()}

    # logging.debug(response["result"]["records"])

    # Constants.db.update({"cities": Constants.cities})
    # Constants.db.update({"cities": unique})


def to_spark_direct_upside_down(cities: dict):
    st = time.time()

    spark_session = SparkSession \
        .builder \
        .enableHiveSupport() \
        .getOrCreate()

    # cities: List[Dict[str, str, str, str, str, str, str, str, str, int]] = dict_root["result"]["records"]
    citiesDF: DataFrame = spark.createDataFrame(data=cities)
    citiesDF.printSchema()
    citiesDF.show(truncate=False)
    # from datetime import date
    # today = date.today()
    # print("Today's date:", today)
    # print(type(citiesDF.filter(citiesDF.Date >= date.today())))
    # filteresDF: DataFrame = citiesDF.filter(citiesDF.Date >= "2021-01-09")
    from datetime import datetime, timedelta
    result_length: int = 0
    day: datetime = datetime.now()  # today
    while result_length == 0:
        # print(type(day))
        day_str: str = datetime.strftime(day, '%Y-%m-%d')
        filteresDF: DataFrame = citiesDF.filter(citiesDF.Date >= day_str)
        filteresDF.show()
        filteresDF.describe().show()
        schema = filteresDF.columns
        logging.debug(schema)
        # print(type(filteresDF.collect()))
        final_result: List[Dict] = filteresDF.collect()
        # print(filteresDF.select("*"))
        # print(datetime.strftime(day, '%Y-%m-%d'), type(datetime.strftime(day, '%Y-%m-%d')))
        logging.debug(f'{day_str} {type(day_str)}')
        logging.debug("Empty RDD: %s" % (final_result.__len__() == 0))
        day = day - timedelta(1)  # timedelta() indicates how many days ago
        result_length = final_result.__len__()
    # print(type(filteresDF.rdd.mapValues(lambda city: (city["City_Name"], city["City_Code"]))))
    # print(filteresDF.rdd.mapValues(lambda city: (city["City_Name"], city["City_Code"])).collectAsMap())
    # print(filteresDF.select(explode(filteresDF.rdd.collectAsMap())))
    # print(explode(filteresDF))
    # print(filteresDF.toPandas().to_dict())
    # my_dict2 = {y: x for x, y in filteresDF.toPandas().to_dict().items()}
    # print(my_dict2)
    # rdd: pyspark.rdd.RDD = sc.parallelize(list)
    def append_json(row: Row):
        # for item in row.asDict(recursive=True).items():
        # my_dict2 = {y: x for x, y in row.asDict(recursive=True).items()}
        # print(my_dict2)
        # print(row.asDict(recursive=True))
        return {row["City_Name"]: row.asDict()} # {"counter": row.asDict()}
        # Constants.json_rows.append({
        #     "City_Code": row["City_Code"],
        #     "City_Name": row.City_Code,
        #     "Cumulated_deaths": row[2]
        # })
    filteresDF.foreach(append_json)
    cities_final_df: DataFrame = spark.createDataFrame(data=filteresDF.rdd.map(append_json).collect())
    # cities_final_df.show()
    #               print(cities_final_df.toPandas().to_dict())
    # print(Constants.json_rows)
    # filteresDF.show()
    # filteresDF.foreachPartition(lambda x: print(x))
   #  metric: Column = create_map(filteresDF.columns)
   #  metric: Column = create_map([
   #      filteresDF.City_Name,
   #      [
   #          filteresDF.City_Code,
   #          filteresDF.Cumulated_deaths,
   #          filteresDF.Cumulated_number_of_diagnostic_tests,
   #          filteresDF.Cumulated_number_of_tests,
   #          filteresDF.Cumulated_recovered,
   #          filteresDF.Cumulated_vaccinated,
   #          filteresDF["Cumulative_verified_cases"],
   #          filteresDF.Date,
   #          filteresDF["_id"]
   #      ]
   #  ])
   #  print(filteresDF.select(explode(metric)))
   #  filteresDF.select(explode(metric)).show()
   #  filteresDF.select(create_map(filteresDF.columns).alias("map")).show()

    Constants.db.update(
        {
            "cities_3": {
                "schema": schema,
                "data": final_result,
                "filteresDF": filteresDF.toJSON().collect(),
                # "ok_3": json.loads(str(dict({"data": filteresDF.toJSON().collect()}))),
                # "ok_5": json.load(filteresDF.toJSON().collect()),
                # "ok": filteresDF.toJSON().keys(),
                # "ok_2": filteresDF.toJSON().collectAsMap(),
                "ok": filteresDF.toPandas().to_dict(),
                "shit": cities_final_df.toPandas().to_dict()
            }
        }
    )  # load to firebase

    Constants.db.update(
        {"cities_final": cities_final_df.toPandas().to_dict()}
    )  # load to firebase
    # ---------------------------------------------------------------------------------
    cities_final_df.summary()

    # Constants.db.update(
    #     {
    #         "israel": {
    #             # "sum": cities_final_df.rdd.sum().__str__(),
    #             "summarize": filteresDF.describe(filteresDF.columns).toPandas().to_dict(),
    #             # "summarize_2": {
    #             #     "City_Code": filteresDF.describe(filteresDF.City_Code).toPandas().to_dict(),
    #             #     "City_Name": filteresDF.describe(filteresDF.City_Name).toPandas().to_dict(),
    #             #     "Cumulated_deaths": filteresDF.describe(filteresDF.Cumulated_deaths).toPandas().to_dict(),
    #             #     "Cumulated_number_of_diagnostic_tests": filteresDF
    #             #         .describe(filteresDF.Cumulated_number_of_diagnostic_tests).toPandas().to_dict(),
    #             #     "Cumulated_number_of_tests": filteresDF
    #             #         .describe(filteresDF.Cumulated_number_of_tests).toPandas().to_dict(),
    #             #     "Cumulated_recovered": filteresDF
    #             #         .describe(filteresDF.Cumulated_recovered).toPandas().to_dict(),
    #             #     "Cumulated_vaccinated": filteresDF
    #             #         .describe(filteresDF.Cumulated_vaccinated).toPandas().to_dict(),
    #             #     "Cumulative_verified_cases": filteresDF
    #             #         .describe(filteresDF.Cumulative_verified_cases).toPandas().to_dict(),
    #             #     "Date": filteresDF.describe(filteresDF.Date).toPandas().to_dict(),
    #             #     "_id": filteresDF.describe(filteresDF["_id"]).toPandas().to_dict(),
    #             # }
    #         }
    #     }
    # )  # load to firebase

    # acc_vaccinated = spark.sparkContext.accumulator(0)
    # acc_vaccinated_less_than_15 = spark.sparkContext.accumulator(0)
    #
    # def count_israel_total(row: Row, acc_vaccinated_internal: Accumulator,
    #                        acc_vaccinated_less_than_15_internal: Accumulator):
    #     # print(row.Cumulated_vaccinated)
    #     if row.Cumulated_vaccinated.isdigit():
    #         acc_vaccinated_internal += int(row.Cumulated_vaccinated)
    #     else:
    #         print(row.Cumulated_vaccinated, type(row.Cumulated_vaccinated))
    #         acc_vaccinated_less_than_15_internal += 1
    #
    # filteresDF.foreach(lambda row: count_israel_total(row, acc_vaccinated, acc_vaccinated_less_than_15))
    # print(acc_vaccinated.value)
    # print(acc_vaccinated_less_than_15.value)
    #
    # Constants.db.update(
    #     {
    #         "israel": {
    #             "Cumulated_vaccinated": acc_vaccinated.value,
    #             "Cumulated_vaccinated_<15": acc_vaccinated_less_than_15.value
    #         }
    #     }
    # )  # load to firebase

    accum_dict: Dict[Dict[str, Accumulator]] = {
        "vaccinated": {
            "Cumulated_vaccinated_total": spark.sparkContext.accumulator(0),
            "Cumulated_vaccinated_<15": spark.sparkContext.accumulator(0)
        },
        "dead": {
            "Cumulated_deaths_total": spark.sparkContext.accumulator(0),
            "Cumulated_deaths_<15": spark.sparkContext.accumulator(0)
        },
        "diagnostic_tests": {
            "Cumulated_number_of_diagnostic_tests_total": spark.sparkContext.accumulator(0),
            "Cumulated_number_of_diagnostic_tests_<15": spark.sparkContext.accumulator(0)
        },
        "tests": {
            "Cumulated_number_of_tests_total": spark.sparkContext.accumulator(0),
            "Cumulated_number_of_tests_<15": spark.sparkContext.accumulator(0)
        },
        "recovered": {
            "Cumulated_recovered_total": spark.sparkContext.accumulator(0),
            "Cumulated_recovered_<15": spark.sparkContext.accumulator(0)
        },
        "Cumulative_verified_cases": {
            "Cumulative_verified_cases_total": spark.sparkContext.accumulator(0),
            "Cumulative_verified_cases_<15": spark.sparkContext.accumulator(0)
        }
    }

    value_accu = spark.sparkContext.accumulator(0)

    def count_israel_total(row: Row, acc_vaccinated_internal: Accumulator,
                           acc_vaccinated_less_than_15_internal: Accumulator):
        # print(row.Cumulated_vaccinated)
        if row.Cumulated_vaccinated.isdigit():
            acc_vaccinated_internal += int(row.Cumulated_vaccinated)
        else:
            print(row.Cumulated_vaccinated, type(row.Cumulated_vaccinated))
            acc_vaccinated_less_than_15_internal += 1

    def switch_accu(key_dict: dict, row: Row, keyname):
        print("----------------------start---------------------------------------")
        print(key_dict, keyname)
        try:
            less_15 = key_dict.popitem()
            cumulated = key_dict.popitem()
            count_israel_total(row, cumulated[1], less_15[1])

            # accum_dict[keyname][cumulated[0]] = cumulated[1].value
            # accum_dict[keyname][less_15[0]] = less_15[1].value
            # print(cumulated[1].value)
            # print(less_15[1].value)
            try:
                print(accum_dict[keyname][cumulated[0]])
            finally:
                print("---------------------end----------------------------------------")
            # for key2 in accum_dict[keyname].keys():
            #     print(accum_dict[keyname], accum_dict[keyname][key2])
            #     accum_dict[keyname][key2] = accum_dict[keyname][key2].value
        except Exception as e:
            logging.error(e)
        # accum_dict[keyname][cumulated[0]] = cumulated[1].value
        # accum_dict[keyname][less_15[0]] = less_15[1].value

    print(accum_dict)

    for key in accum_dict.keys():
        print(key, accum_dict[key])
        filteresDF.foreach(lambda row: switch_accu(key_dict=accum_dict[key], row=row, keyname=key))
        for key2 in accum_dict[key].keys():
            print(accum_dict[key], accum_dict[key][key2].value)
            accum_dict[key][key2] = accum_dict[key][key2].value
    #
    # Constants.db.update(
    #     {
    #         "israel": accum_dict
    #     }
    # )  # load to firebase

    Constants.db.update(
        {
            "israel": {
                str(accum_dict["vaccinated"]): {
                    "Cumulated_vaccinated_total": accum_dict["vaccinated"]["Cumulated_vaccinated_total"],
                    "Cumulated_vaccinated_<15": accum_dict["vaccinated"]["Cumulated_vaccinated_<15"]
                },
                str(accum_dict["dead"]): {
                    "Cumulated_deaths_total": accum_dict["dead"]["Cumulated_deaths_total"],
                    "Cumulated_deaths_<15": accum_dict["dead"]["Cumulated_deaths_<15"]
                },
                str(accum_dict["diagnostic_tests"]): {
                    "Cumulated_number_of_diagnostic_tests_total":
                        accum_dict["diagnostic_tests"]["Cumulated_number_of_diagnostic_tests_total"],
                    "Cumulated_number_of_diagnostic_tests_<15":
                        accum_dict["diagnostic_tests"]["Cumulated_number_of_diagnostic_tests_<15"]
                },
                str(accum_dict["tests"]): {
                    "Cumulated_number_of_tests_total": accum_dict["tests"]["Cumulated_number_of_tests_total"],
                    "Cumulated_number_of_tests_<15": accum_dict["tests"]["Cumulated_number_of_tests_<15"]
                },
                str(accum_dict["recovered"]): {
                    "Cumulated_recovered_total": accum_dict["recovered"]["Cumulated_recovered_total"],
                    "Cumulated_recovered_<15": accum_dict["recovered"]["Cumulated_recovered_<15"]
                },
                str(accum_dict["Cumulative_verified_cases"]): {
                    "Cumulative_verified_cases_total":
                        accum_dict["Cumulative_verified_cases"]["Cumulative_verified_cases_total"],
                    "Cumulative_verified_cases_<15":
                        accum_dict["Cumulative_verified_cases"]["Cumulative_verified_cases_<15"]
                },
            }
        }
    )  # load to firebase

    # from testsAndOthers.data_types_and_structures import DataTypesHandler, PrintForm
    # DataTypesHandler.print_data_recursively(data=json_count_names, print_dict=PrintForm.PRINT_DICT.value)

    logging.debug(f"spark total time: {time.time() - st} seconds")


def to_spark_direct(cities: dict):
    st = time.time()

    spark_session = SparkSession \
        .builder \
        .enableHiveSupport() \
        .getOrCreate()

    # cities: List[Dict[str, str, str, str, str, str, str, str, str, int]] = dict_root["result"]["records"]
    citiesDF: DataFrame = spark.createDataFrame(data=cities)
    citiesDF.printSchema()
    citiesDF.show(truncate=False)
    # from datetime import date
    # today = date.today()
    # print("Today's date:", today)
    # print(type(citiesDF.filter(citiesDF.Date >= date.today())))
    # filteresDF: DataFrame = citiesDF.filter(citiesDF.Date >= "2021-01-09")
    from datetime import datetime, timedelta
    result_length: int = 0
    day: datetime = datetime.now()  # today
    while result_length == 0:
        # print(type(day))
        day_str: str = datetime.strftime(day, '%Y-%m-%d')
        filteresDF: DataFrame = citiesDF.filter(citiesDF.Date >= day_str)
        filteresDF.show()
        filteresDF.describe().show()
        schema = filteresDF.columns
        logging.debug(schema)
        # print(type(filteresDF.collect()))
        final_result: List[Dict] = filteresDF.collect()
        # print(filteresDF.select("*"))
        # print(datetime.strftime(day, '%Y-%m-%d'), type(datetime.strftime(day, '%Y-%m-%d')))
        logging.debug(f'{day_str} {type(day_str)}')
        logging.debug("Empty RDD: %s" % (final_result.__len__() == 0))
        day = day - timedelta(1)  # timedelta() indicates how many days ago
        result_length = final_result.__len__()
    # print(type(filteresDF.rdd.mapValues(lambda city: (city["City_Name"], city["City_Code"]))))
    # print(filteresDF.rdd.mapValues(lambda city: (city["City_Name"], city["City_Code"])).collectAsMap())
    # print(filteresDF.select(explode(filteresDF.rdd.collectAsMap())))
    # print(explode(filteresDF))
    # print(filteresDF.toPandas().to_dict())
    my_dict2 = {y: x for x, y in filteresDF.toPandas().to_dict().items()}
    print(my_dict2)
   #  metric: Column = create_map(filteresDF.columns)
   #  metric: Column = create_map([
   #      filteresDF.City_Name,
   #      [
   #          filteresDF.City_Code,
   #          filteresDF.Cumulated_deaths,
   #          filteresDF.Cumulated_number_of_diagnostic_tests,
   #          filteresDF.Cumulated_number_of_tests,
   #          filteresDF.Cumulated_recovered,
   #          filteresDF.Cumulated_vaccinated,
   #          filteresDF["Cumulative_verified_cases"],
   #          filteresDF.Date,
   #          filteresDF["_id"]
   #      ]
   #  ])
   #  print(filteresDF.select(explode(metric)))
   #  filteresDF.select(explode(metric)).show()
   #  filteresDF.select(create_map(filteresDF.columns).alias("map")).show()

    Constants.db.update(
        {
            "cities_3": {
                "schema": schema,
                "data": final_result,
                "filteresDF": filteresDF.toJSON().collect(),
                # "ok_3": json.loads(str(dict({"data": filteresDF.toJSON().collect()}))),
                # "ok_5": json.load(filteresDF.toJSON().collect()),
                # "ok": filteresDF.toJSON().keys(),
                # "ok_2": filteresDF.toJSON().collectAsMap(),
                "ok": filteresDF.toPandas().to_dict()
            }
        }
    )  # load to firebase

    # from testsAndOthers.data_types_and_structures import DataTypesHandler, PrintForm
    # DataTypesHandler.print_data_recursively(data=json_count_names, print_dict=PrintForm.PRINT_DICT.value)

    logging.debug(f"spark total time: {time.time() - st} seconds")


def to_spark():
    st = time.time()

    spark_session = SparkSession \
        .builder \
        .enableHiveSupport() \
        .getOrCreate()

    df: DataFrame = spark_session.read.json("json/city_json.json")
    df.show()

    df.createOrReplaceTempView("table_1")

    df2: DataFrame = spark.sql("SELECT result from table_1")

    df2.show()

    rdd: RDD = df2.toJSON()
    print(rdd.count())

    first_elem: str = rdd.first()

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
    # print(type(filteresDF.collect()))
    final_result: List[Dict] = filteresDF.collect()

    Constants.db.update({"cities_2": final_result})  # load to firebase

    # from testsAndOthers.data_types_and_structures import DataTypesHandler, PrintForm
    # DataTypesHandler.print_data_recursively(data=json_count_names, print_dict=PrintForm.PRINT_DICT.value)

    logging.debug(f"spark total time: {time.time() - st} seconds")


@Constants.SCHEDULER.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=0, second=0)
def scheduled_job():
    print('This job is run every weekday at 7am.')
    firebase_config()
    crawl_corona()
    # to_spark()
    print(datetime.datetime.now())
    winsound.MessageBeep(winsound.MB_OK)


# TODO: load json using spark & save to hdfs, sqlite, elastic & ml? mining? cluster?
def main():
    st = time.time()

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('flaskwebgui').setLevel(logging.ERROR)
    logging.getLogger('BaseHTTPRequestHandler').setLevel(logging.ERROR)
    logging.getLogger('matplotlib').setLevel(logging.ERROR)
    logging.getLogger('py4j').setLevel(logging.ERROR)
    logging.getLogger('my_log').setLevel(logging.DEBUG)

    try:
        # Constants.SCHEDULER.start()
        firebase_config()
        crawl_corona()
        # to_spark()
    finally:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        logging.debug(f"Program Total Time: {time.time() - st} seconds")


if __name__ == '__main__':
    main()
