import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("secret.json")
databaseURL = "https://finalyearproject-d2b17-default-rtdb.firebaseio.com/"
firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
    })


ref = db.reference("/")

print(ref.get())
