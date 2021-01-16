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
    # TODO: catch if there is no internet connection
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
    # citiesDF.printSchema()
    # citiesDF.show(truncate=False)

    from datetime import datetime, timedelta
    result_length: int = 0
    day: datetime = datetime.now()  # today
    while result_length == 0:
        day_str: str = datetime.strftime(day, '%Y-%m-%d')
        filteresDF: DataFrame = citiesDF.filter(citiesDF.Date >= day_str)
        # filteresDF.show()
        # filteresDF.describe().show()
        schema = filteresDF.columns
        # logging.debug(schema)

        final_result: List[Dict] = filteresDF.collect()

        logging.debug(f'{day_str} {type(day_str)}')
        logging.debug("Empty RDD: %s" % (final_result.__len__() == 0))
        day = day - timedelta(1)  # timedelta() indicates how many days ago
        result_length = final_result.__len__()

    def append_json(row: Row):
        return {row["City_Name"]: row.asDict()}  # {"counter": row.asDict()}

    filteresDF.foreach(append_json)
    cities_final_df: DataFrame = spark.createDataFrame(data=filteresDF.rdd.map(append_json).collect())
    # print(cities_final_df.toPandas().to_dict())

    Constants.db.update(
        {
            "cities_3": {
                "schema": schema,
                "data": final_result,
                "filteresDF": filteresDF.toJSON().collect(),
                "ok": filteresDF.toPandas().to_dict(),
                "shit": cities_final_df.toPandas().to_dict()
            }
        }
    )  # load to firebase

    Constants.db.update(
        {"cities_final": cities_final_df.toPandas().to_dict()}
    )  # load to firebase
    # ---------------------------------------------------------------------------------
    # cities_final_df.summary()

    # print(filteresDF.toPandas().to_dict()["Cumulated_vaccinated"])
    # print(filteresDF.Cumulated_vaccinated)
    # vaccinated: Column = filteresDF.Cumulated_vaccinated
    # vaccinated_df: DataFrame = spark.createDataFrame(data=vaccinated)
    # vaccinated_df.show()

    # filteresDF.select(filteresDF.Cumulated_vaccinated).show()

    total: Accumulator = spark.sparkContext.accumulator(0)
    less: Accumulator = spark.sparkContext.accumulator(0)
    keys_lst: list = []
    updated_to: str = ''

    def add(row: Row, total: Accumulator, less: Accumulator):
        # print(row.asDict().values())
        for val in row.asDict().values():
            if str(val).isdigit():
                total += int(val)
            elif val == "<15":
                less += 1

    for key in filteresDF.toPandas().keys():
        if key == 'Date':
            # print(filteresDF[key].getItem(0).astype("strןמע"))
            print(filteresDF.rdd.first().Date)
            updated_to = filteresDF.rdd.first().Date
            continue
        elif key in ["_id", "City_Name", "City_Code"]: continue
        print(key)
        filteresDF.select(filteresDF[key]).foreach(lambda row: add(row, total, less))
        print(total.value)
        print(less.value)
        keys_lst.append(
            {
                str(key): {
                    "total": total.value,
                    "less_<15": less.value
                }
            }
        )
        total.value = 0
        less.value = 0

    keys_lst.append(updated_to)
    Constants.db.update(
        {
            "israel_final_3": keys_lst
        }
    )

    Constants.db.update(
        {
            "israel_final_2": [
                keys_lst, updated_to
            ]
        }
    )

    Constants.db.update(
        {
            "israel_final": {
                "data": keys_lst,
                "Last_Update": updated_to
            }
        }
    )

    # accum_dict: Dict[Dict[str, Accumulator]] = {
    #     "vaccinated": {
    #         "Cumulated_vaccinated_total": spark.sparkContext.accumulator(0),
    #         "Cumulated_vaccinated_<15": spark.sparkContext.accumulator(0)
    #     },
    #     "dead": {
    #         "Cumulated_deaths_total": spark.sparkContext.accumulator(0),
    #         "Cumulated_deaths_<15": spark.sparkContext.accumulator(0)
    #     },
    #     "diagnostic_tests": {
    #         "Cumulated_number_of_diagnostic_tests_total": spark.sparkContext.accumulator(0),
    #         "Cumulated_number_of_diagnostic_tests_<15": spark.sparkContext.accumulator(0)
    #     },
    #     "tests": {
    #         "Cumulated_number_of_tests_total": spark.sparkContext.accumulator(0),
    #         "Cumulated_number_of_tests_<15": spark.sparkContext.accumulator(0)
    #     },
    #     "recovered": {
    #         "Cumulated_recovered_total": spark.sparkContext.accumulator(0),
    #         "Cumulated_recovered_<15": spark.sparkContext.accumulator(0)
    #     },
    #     "Cumulative_verified_cases": {
    #         "Cumulative_verified_cases_total": spark.sparkContext.accumulator(0),
    #         "Cumulative_verified_cases_<15": spark.sparkContext.accumulator(0)
    #     }
    # }
    #
    # def count_israel_total(row: Row, acc_vaccinated_internal: Accumulator,
    #                        acc_vaccinated_less_than_15_internal: Accumulator):
    #     # print(row)
    #     for city in row.asDict().values():
    #         print(city)
    #     if row.Cumulated_vaccinated.isdigit():
    #         acc_vaccinated_internal += int(row.Cumulated_vaccinated)
    #         # print(f"------------------{int(row.Cumulated_vaccinated)}-----------------------")
    #     else:
    #         print(row.Cumulated_vaccinated, type(row.Cumulated_vaccinated))
    #         print("------------------<15-----------------------")
    #         acc_vaccinated_less_than_15_internal += 1
    #
    # def switch_accu(key_dict: dict, row: Row, keyname):
    #     # print(key_dict, keyname)
    #     try:
    #         less_15 = key_dict.popitem()
    #         cumulated = key_dict.popitem()
    #         count_israel_total(row, cumulated[1], less_15[1])
    #
    #     except Exception as e:
    #         # logging.error(e)
    #         pass
    #     finally:
    #         # print()
    #         pass
    #
    # # print(accum_dict)
    #
    # for key in accum_dict.keys():
    #     # print(key, accum_dict[key])
    #     cities_final_df.foreach(lambda row: switch_accu(key_dict=accum_dict[key], row=row, keyname=key))
    #
    #     for key2 in accum_dict[key].keys():
    #         # print(accum_dict[key], accum_dict[key][key2].value)
    #         accum_dict[key][key2] = accum_dict[key][key2].value
    #
    # Constants.db.update(
    #     {
    #         "israel": {
    #             str(accum_dict["vaccinated"]): {
    #                 "Cumulated_vaccinated_total": accum_dict["vaccinated"]["Cumulated_vaccinated_total"],
    #                 "Cumulated_vaccinated_<15": accum_dict["vaccinated"]["Cumulated_vaccinated_<15"]
    #             },
    #             str(accum_dict["dead"]): {
    #                 "Cumulated_deaths_total": accum_dict["dead"]["Cumulated_deaths_total"],
    #                 "Cumulated_deaths_<15": accum_dict["dead"]["Cumulated_deaths_<15"]
    #             },
    #             str(accum_dict["diagnostic_tests"]): {
    #                 "Cumulated_number_of_diagnostic_tests_total":
    #                     accum_dict["diagnostic_tests"]["Cumulated_number_of_diagnostic_tests_total"],
    #                 "Cumulated_number_of_diagnostic_tests_<15":
    #                     accum_dict["diagnostic_tests"]["Cumulated_number_of_diagnostic_tests_<15"]
    #             },
    #             str(accum_dict["tests"]): {
    #                 "Cumulated_number_of_tests_total": accum_dict["tests"]["Cumulated_number_of_tests_total"],
    #                 "Cumulated_number_of_tests_<15": accum_dict["tests"]["Cumulated_number_of_tests_<15"]
    #             },
    #             str(accum_dict["recovered"]): {
    #                 "Cumulated_recovered_total": accum_dict["recovered"]["Cumulated_recovered_total"],
    #                 "Cumulated_recovered_<15": accum_dict["recovered"]["Cumulated_recovered_<15"]
    #             },
    #             str(accum_dict["Cumulative_verified_cases"]): {
    #                 "Cumulative_verified_cases_total":
    #                     accum_dict["Cumulative_verified_cases"]["Cumulative_verified_cases_total"],
    #                 "Cumulative_verified_cases_<15":
    #                     accum_dict["Cumulative_verified_cases"]["Cumulative_verified_cases_<15"]
    #             },
    #         }
    #     }
    # )  # load to firebase

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
