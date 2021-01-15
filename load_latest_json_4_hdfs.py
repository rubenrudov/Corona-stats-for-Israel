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
    to_spark_direct_upside_down(cities=response["result"]["records"])


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

        schema = filteresDF.columns

        final_result: List[Dict] = filteresDF.collect()

        logging.debug(f'{day_str} {type(day_str)}')
        logging.debug("Empty RDD: %s" % (final_result.__len__() == 0))
        day = day - timedelta(1)  # timedelta() indicates how many days ago
        result_length = final_result.__len__()

    # filteresDF.show()
    # filteresDF.describe().show()
    # logging.debug(schema)

    def append_json(row: Row):
        return {row["City_Name"]: row.asDict()}  # {"counter": row.asDict()}

    filteresDF.foreach(append_json)
    cities_final_df: DataFrame = spark.createDataFrame(data=filteresDF.rdd.map(append_json).collect())

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

    total: Accumulator = spark.sparkContext.accumulator(0)
    less: Accumulator = spark.sparkContext.accumulator(0)
    keys_lst: list = []
    updated_to: str = ''

    def add(row: Row, total: Accumulator, less: Accumulator):
        for val in row.asDict().values():
            if str(val).isdigit():
                total += int(val)
            elif val == "<15":
                less += 1

    for key in filteresDF.toPandas().keys():
        if key == 'Date':
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

    logging.debug(f"spark total time: {time.time() - st} seconds")


@Constants.SCHEDULER.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=0, second=0)
def scheduled_job():
    print('This job is run every weekday at 7am.')
    firebase_config()
    crawl_corona()
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
    finally:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        logging.debug(f"Program Total Time: {time.time() - st} seconds")


if __name__ == '__main__':
    main()
