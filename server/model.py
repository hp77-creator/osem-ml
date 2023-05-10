from keras.models import Sequential
import pickle
from datetime import datetime as dt
from scipy.stats import zscore
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import numpy as np

def create_model(shape, optimizer):
    model = tf.keras.Sequential()
    model.add(layers.Dense(shape, activation=tf.nn.relu, input_shape=[71])) # x ki shape 31 hai 
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(1))
    model.compile(loss="mean_squared_error",optimizer=optimizer,metrics=["mean_absolute_error", "mean_squared_error"])
    return model

def makeUsefulDf(df, noise=2.5, hours_prior=24):
    if 'dates' not in df.columns:
        df['dates'] = df.apply(lambda x: dt(int(x['year']), int(x['month']), int(x['day']), int(x['hour'])), axis=1)
    
    #PREV LOAD & LOAD
    r_df = pd.DataFrame()
    r_df["loads_n"] = zscore(df["load"])
    r_df["loads_prev_n"] = r_df["loads_n"].shift(hours_prior)
    r_df["loads_prev_n"].bfill(inplace=True)
    #LOAD PREV
    # print(r_df.head())
    def _chunks(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]
    
    n = np.array([val for val in _chunks(list(r_df["loads_n"]), hours_prior) for _ in range(hours_prior)])
    #print(n)
    l = ["l" + str(i) for i in range(24)]
    if n.shape[1] >= 24:
        for i, s in enumerate(l):
            r_df[s] = n[:, i]
            r_df[s] = r_df[s].shift(hours_prior)
            r_df[s] = r_df[s].bfill()
    else:
        for i, s in enumerate(l):
            r_df[s] = n[:, 0]
            r_df[s] = r_df[s].shift(hours_prior)
            r_df[s] = r_df[s].bfill()
    r_df.drop(['loads_n'], axis=1, inplace=True)
    #Date
    r_df["years_n"] = zscore(df["dates"].dt.year)
    r_df = pd.concat([r_df, pd.get_dummies(df.dates.dt.hour, prefix='hour')], axis=1)
    r_df = pd.concat([r_df, pd.get_dummies(df.dates.dt.dayofweek, prefix='day')], axis=1)
    r_df = pd.concat([r_df, pd.get_dummies(df.dates.dt.month, prefix='month')], axis=1)

    col_lis = ['loads_prev_n', 'l0', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8',
       'l9', 'l10', 'l11', 'l12', 'l13', 'l14', 'l15', 'l16', 'l17', 'l18',
       'l19', 'l20', 'l21', 'l22', 'l23', 'years_n', 'hour_0', 'hour_1',
       'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8',
       'hour_9', 'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14',
       'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20',
       'hour_21', 'hour_22', 'hour_23', 'day_0', 'day_1', 'day_2', 'day_3',
       'day_4', 'day_5', 'day_6', 'month_1', 'month_2', 'month_3', 'month_4',
       'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10',
       'month_11', 'month_12', 'temp_n', 'temp_n^2']
    for i in col_lis:
        if i not in r_df.keys():
            r_df[i] = 0
    #I am not excluding holidays
    #for holiday in ["New Year's Day", "Memorial Day", "Independence Day", "Labor Day", "Thanksgiving", "Christmas Day"]:
    #r_df[holiday] = _isHoliday(holiday, df)


    
    #including noise in the data
    temp_noise = df['tempc'] + np.random.normal(0, noise, df.shape[0])
    r_df["temp_n"] = zscore(temp_noise)
    r_df['temp_n^2'] = zscore([x*x for x in temp_noise])
    print(r_df.select_dtypes(np.float64).columns)
    r_df[r_df.select_dtypes(np.float64).columns] = r_df.select_dtypes(np.float64).astype(np.float32)
    print(r_df.select_dtypes(np.float64).columns)
    return r_df

