from firebase import Firebase
# https://bitbucket.org/joetilsed/firebase/src/master/firebase/__init__.py
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

db = firebase.database()
# print(db.child("users").get())

# users = db.child("users").get()
# print(users.val())
#
# user = db.child("users").get()
# print(user.key())
#
# users = db.child("Stats").get()
# print(users.val())
#
# # data = {"Corona": "my corona bitch"}
# # db.child("Stats").push(data)
#
# db.child("Stats").child("Corona").remove()
#
# users = db.child("Stats").get()
# print(users.val())
#
# all_user_ids = db.child("Stats").shallow().get()
# print(all_user_ids)
#
# users = db.child("Stats").get()
# print(users.val())
#
# # db.child("Stats").child("-MQmBJyn_Vy3GPrJHp_n").remove()
# # db.child("Stats").child("-MQmBPucWMGFVg7wW-v5").remove()
#
# data = {"Corona": "my corona"}
# db.child("Stats").push(["data", data])
# db.child("Stats").child("-MQmC_1BmrYYmpZFwSHZ").remove()
#
# db.child("Stats").push({"israel": "5885"})

# stats = db.child("Stats").get()
# print(stats.val())
# print(stats.key())
# print(stats)
# print(stats.each())
# print(stats.firebases())
# print(stats.query_key())

# stats = db.child("Stats").child({"israel_adam": "0"})
# stats_2 = db.get()
# print(stats_2.val())

# print(db.child("Stats").get().val())
# for stat in db.child("Stats").get().val().values():
#    stats_list.append(stat)
#    print(stat)

# # create database
# db.push({
#     "Stats": {
#         "cityIdRandom": {
#             "name": "city",
#             "code": 1,
#             "numOfSick": 20
#         }
#     }
# })

# print database
# recurse?
stats_list = []

for stat in db.get().val().values():
    stats_list.append(stat)
    print(stat)

print(db.get().val())
print(stats_list)

# for stat in db.get().val().values():
#     print(stat["Stats"]['cityIdRandom']['name'])
