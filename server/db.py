import firebase_admin
from firebase_admin import credentials, db
import json
import pandas as pd

cred = credentials.Certificate("secret.json")
databaseURL = "https://finalyearproject-d2b17-default-rtdb.firebaseio.com/"
firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
    })



# ref = db.reference("/users_v1/Dk1Z5a2Tdxe0jx1njiLlsEdv10t1/") # only get data of a single user
ref = db.reference("/users_v1/Dk1Z5a2Tdxe0jx1njiLlsEdv10t1/123295615518260_ESP32-D0WDQ5/0/data") # only get data of a single user's single room

json_obj = ref.get()
json_string = json.dumps(json_obj)
#print(json_string)

#print(json_obj)
#df = pd.read_json(json_obj)
#print(df.head())
with open('data.json', 'w') as f:
    json.dump(json_obj, f)

df = pd.read_json('data.json')
df_t = df.T
df_t['value'] = df_t['value']*220
df_t['date'] = pd.to_datetime(df_t['Ts'],unit='ms')
df_t['year'] = pd.DatetimeIndex(df_t['date']).year
df_t['month'] = pd.DatetimeIndex(df_t['date']).month
df_t['day'] = pd.DatetimeIndex(df_t['date']).day
df_t['hour'] = pd.DatetimeIndex(df_t['date']).hour
df_t['tempc'] = 25 # using a constant value for temperature at the moment
df_t_new = df_t.drop(['date', 'Ts'], axis=1)
df_t_new = df_t_new.rename({'value': 'load'}, axis=1)

df_t_new.to_csv('data.csv', index=False)

# print(df_t_new.head())

# df_t.to_csv('data.csv')

#df_t = pd.read_csv('data.csv')



