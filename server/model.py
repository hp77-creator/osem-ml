from keras.models import Sequential
import pickle
from datetime import datetime as dt
from scipy.stats import zscore
import tensorflow as tf
from tensorflow.keras import layers

def create_model(shape, optimizer):
    model = tf.keras.Sequential()
    model.add(layers.Dense(shape, activation=tf.nn.relu, input_shape=[len(x.keys())]))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(shape, activation=tf.nn.relu))
    model.add(layers.Dense(1))
    model.compile(loss="mean_squared_error",optimizer=optimizer,metrics=["mean_absolute_error", "mean_squared_error"])
    return model


