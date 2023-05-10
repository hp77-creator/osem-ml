import firebase_admin
from firebase_admin import credentials, db
import json

cred = credentials.Certificate("secret.json")
databaseURL = "https://finalyearproject-d2b17-default-rtdb.firebaseio.com/"
firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
    })


ref = db.reference("/users_v1/Dk1Z5a2Tdxe0jx1njiLlsEdv10t1/") # only get data of users device

json_obj = ref.get()

with open('data.json', 'w') as f:
    json.dump(json_obj, f)



