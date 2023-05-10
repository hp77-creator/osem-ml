from typing import Union
from fastapi import FastAPI

from keras.models import Sequential
import pickle
from datetime import datetime as dt
from scipy.stats import zscore
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras import layers
from xgboost import XGBRegressor

from model import create_model, makeUsefulDf

app = FastAPI()

# general model
@app.get('/ml')
def read_ml():
    SHAPE=71 # number of columns in our dataframe
    optimizer=tf.keras.optimizers.RMSprop(0.0001)
    df = pd.read_csv('../data.csv')
    #print(df.head())
    x = makeUsefulDf(df, hours_prior=1) 
    reg = XGBRegressor()
    reg.fit(x, df['load'])
    #print(x.keys())
    #x = np.asarray(x).astype(np.float32)
    #print(type(x))
    #model = create_model(SHAPE, optimizer)
    #model.load_weights('../ml-model/modelFP.h5')
    #prediction = model.predict(x.iloc[[0]])
    #if pred
    #print(prediction)
    prediction = reg.predict(x.iloc[[0]])[0]
    print(prediction)
    return {"prediction": str(prediction)}
    
    
