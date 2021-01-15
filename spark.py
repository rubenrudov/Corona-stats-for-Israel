import json
from urllib.request import urlopen

import requests
from pyspark.shell import sqlContext, sc


def convert_single_object_per_line(json_list):
    json_string = ""
    for line in json_list:
        json_string += json.dumps(line) + "\n"
    return json_string


def parse_dataframe(json_data):
    print(json_data)
    r = convert_single_object_per_line(json_data)
    mylist = []
    for line in r.splitlines():
        mylist.append(line)
    rdd = sc.parallelize(mylist)
    df = sqlContext.jsonRDD(rdd)
    return df


URL_GOV = 'https://data.gov.il/api/3/action/datastore_search?' \
          'resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&limit=1000000000'
# response = urlopen(URL_GOV)
response: dict = requests.get(URL_GOV).json()
# data = str(response.__str__())
# json_data = json.load(response)
# print(response)
# df = parse_dataframe(response["result"]["records"])

import json
import requests
# df = sqlContext.createDataFrame([json.loads(line) for line in response.values()])
for line in response["result"]["records"]:
    print(line)

# {
#     "help": "https://data.gov.il/api/3/action/help_show?name=datastore_search",
#     "success": true,
#     "result": {
#         "include_total": false,
#         "resource_id": "8a21d39d-91e3-40db-aca1-f73f7ab1df69",
#         "fields": [
#             {"type": "int", "id": "_id"},
#             {"type": "text", "id": "City_Name"},
#             {"type": "text", "id": "City_Code"},
#             {"type": "text", "id": "Date"},
#             {"type": "text", "id": "Cumulative_verified_cases"},
#             {"type": "text", "id": "Cumulated_recovered"},
#             {"type": "text", "id": "Cumulated_deaths"},
#             {"type": "text", "id": "Cumulated_number_of_tests"},
#             {"type": "text", "id": "Cumulated_number_of_diagnostic_tests"},
#             {"type": "text", "id": "Cumulated_vaccinated"}
#         ],
#         "records_format": "objects",
#         "records": [
#             {"_id": 1, "City_Name": "\u05d0\u05d1\u05d5 \u05d2'\u05d5\u05d5\u05d9\u05d9\u05e2\u05d3 (\u05e9\u05d1\u05d8)", "City_Code": "967", "Date": "2020-03-11", "Cumulative_verified_cases": "0", "Cumulated_recovered": "0", "Cumulated_deaths": "0", "Cumulated_number_of_tests": "0", "Cumulated_number_of_diagnostic_tests": "0", "Cumulated_vaccinated": "0"},
#             {"_id": 2, "City_Name": "\u05d0\u05d1\u05d5 \u05d2'\u05d5\u05d5\u05d9\u05d9\u05e2\u05d3 (\u05e9\u05d1\u05d8)", "City_Code": "967", "Date": "2020-03-12", "Cumulative_verified_cases": "0", "Cumulated_recovered": "0", "Cumulated_deaths": "0", "Cumulated_number_of_tests": "0", "Cumulated_number_of_diagnostic_tests": "0", "Cumulated_vaccinated": "0"}
#             ...
#             ...
#             ...
#         ]
#     }
# }


# {
#     "result":{
#         "_links":{
#             "next":"/api/3/action/datastore_search?offset=1000000000&limit=1000000000&resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69",
#             "start":"/api/3/action/datastore_search?limit=1000000000&resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69"
#         },
#         "fields":[
#             {"id":"_id","type":"int"},
#             {"id":"City_Name","type":"text"},
#             {"id":"City_Code","type":"text"},
#             {"id":"Date","type":"text"},
#             {"id":"Cumulative_verified_cases","type":"text"},
#             {"id":"Cumulated_recovered","type":"text"}
#         ],
#         "include_total":false,
#         "limit":1000000000,
#         "records":[
#             {"City_Code":"967","City_Name":"אבו ג'ווייעד (שבט)","Cumulated_deaths":"0","Cumulated_number_of_diagnostic_tests":"0","Cumulated_number_of_tests":"0","Cumulated_recovered":"0","Cumulated_vaccinated":"0","Cumulative_verified_cases":"0","Date":"2020-03-11","_id":1},
#             ....