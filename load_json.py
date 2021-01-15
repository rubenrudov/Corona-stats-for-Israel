import datetime
import logging
import winsound

import requests as requests
from firebase import Firebase

from apscheduler.schedulers.blocking import BlockingScheduler
# https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# https://data.gov.il/dataset/covid-19/resource/0995c344-6a7a-4557-99ff-28ee6f3149b3
# https://data.gov.il/dataset/covid-19/resource/89f61e3a-4866-4bbf-bcc1-9734e5fee58e
# https://console.firebase.google.com/u/2/project/corona-charts-33e8a/database/corona-charts-33e8a-default-rtdb/data/~2F


class Constants:
    cities = []
    city_code = -1
    ret = {}
    db = {}
    URL_GOV = 'https://data.gov.il/api/3/action/datastore_search?' \
              'resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&limit=100000000'
    SCHEDULER: BlockingScheduler = BlockingScheduler()


def filter_line(json_line):
    # print(json_line)

    if not Constants.city_code == json_line["City_Code"]:
        Constants.ret.clear()
        Constants.cities.append(json_line)
    # else:

        # for city in Constants.cities:
        #     print(json_line["City_Code"] > city["City_Code"])
        #     if json_line["City_Code"] > city["City_Code"]:

    # elif json_line["City_Code"] in Constants.cities:
    #     for city in Constants.cities:
    #         print(json_line["City_Code"] > city["City_Code"])

    Constants.city_code = json_line["City_Code"]


# def filter_line(json_line):
#     # print(json_line)
#
#     if not Constants.city_code == json_line["City_Code"]:
#         Constants.ret.clear()
#         Constants.cities.append(json_line)
#     else:
#         for city in Constants.cities:
#             # print(json_line["Date"])
#             try:
#                 if json_line["Date"] > Constants.ret["Date"]:
#                     Constants.ret = {
#                         "_id": json_line["_id"], 'City_Name': json_line['City_Name'],
#                         'City_Code': json_line['City_Code'], 'Date': json_line['Date']
#                     }
#             except:
#                 Constants.ret = {
#                     "_id": json_line["_id"], 'City_Name': json_line['City_Name'],
#                     'City_Code': json_line['City_Code'], 'Date': json_line['Date']
#                 }
#
#     Constants.city_code = json_line["City_Code"]
#     return Constants.ret


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
    cities_list = []

    counter = 0
    for line in response["result"]["records"]:
        counter +=1
        # print(line)
        json_filtered: dict = filter_line(line)
        cities_list.append(json_filtered)
        # Constants.ret.clear()
        # print(json_filtered)
    # print(Constants.cities)

    logging.debug(f"number of rows: {counter}")
    names = []
    unique = []
    # for city in cities_list:
    #     # print(city)
    #     try:
    #         if city['City_Code'] in names: raise Exception()
    #         # print(city['City_Code'])
    #         names.append(city['City_Code'])
    #         unique.append(city)
    #     except:
    #         pass

    # print(unique)
    Constants.db.update({"cities": Constants.cities})
    # Constants.db.update({"cities": unique})


# db.push({"cities": unique})
# db.child("-MQsJmMSDequQrEca5Ff").remove()
#
# for stat in db.get().val().values():
#     db.child("-MQqph8bGa-ihU7gIcIs").remove()
#    db.child("-MQsECeGiRUYXKKg-P_h").push({"cities": unique})

# db.push({
#     "Stats": {
#         "cityIdRandom": {
#             "name": "city",
#             "code": 1,
#             "numOfSick": 20
#         }
#     }
# })

@Constants.SCHEDULER.scheduled_job('cron', day_of_week='mon-sun', hour=14, minute=15, second=30)
def scheduled_job():
    print('This job is run every weekday at 0am.')
    firebase_config()
    crawl_corona()
    print(datetime.datetime.now())
    winsound.MessageBeep(winsound.MB_OK)


# TODO: load json using spark & save to hdfs, sqlite, elastic & ml? mining? cluster?
def main():
    logging.basicConfig(level=logging.DEBUG)
    # Constants.SCHEDULER.start()

    firebase_config()
    crawl_corona()

    winsound.MessageBeep(winsound.MB_ICONHAND)


if __name__ == '__main__':
    main()

    # winsound.MessageBeep(winsound.MB_OK)
    # winsound.Beep(10000, 1000)
    # winsound.MessageBeep(winsound.MB_ICONHAND)
    # winsound.PlaySound("SystemHand", 0)
    # winsound.PlaySound("SystemQuestion", 0)
