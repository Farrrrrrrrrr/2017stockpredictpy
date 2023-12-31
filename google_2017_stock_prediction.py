# -*- coding: utf-8 -*-
"""Google 2017 stock prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H-r6mXfagC9jA4OMlzTRr9zv7IU8gfEU
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

data = pd.read_csv("Google_train_data.csv")
data.head()

data["Close"]=pd.to_numeric(data.Close,errors='coerce')
data = data.dropna()
trainData = data.iloc[:,4:5].values

data.info()

sc = MinMaxScaler(feature_range=(0,1))
trainData = sc.fit_transform(trainData)
trainData.shape

X_train = []
y_train = []

for i in range (60,1149):
  X_train.append(trainData[i-60:i,0])
  y_train.append(trainData[i,0])

X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_train.shape

model = Sequential()

model.add(LSTM(units = 100, return_sequences=True, input_shape = (X_train.shape[1], 1)))
model.add(Dropout(0.2))

model.add(LSTM(units = 100, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units = 100, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units = 100))
model.add(Dropout(0.2))

model.add(Dense(units=1))
model.compile(optimizer='adam', loss="mean_squared_error")

hist = model.fit(X_train, y_train, epochs = 20, batch_size =32, verbose=2)

plt.plot(hist.history['loss'])
plt.title('Model Training for Loss')
plt.xlabel('Epoch')
plt.ylabel('loss')
plt.legend(['train'], loc='upper left')
plt.show()

testData = pd.read_csv('Google_test_data.csv')
testData["Close"]=pd.to_numeric(testData.Close,errors='coerce')
testData = testData.dropna()
testData = testData.iloc[:,4:5]
y_test = testData.iloc[60:,0:].values
inputClosing = testData.iloc[:,0:].values
inputClosing_scaled = sc.transform(inputClosing)
inputClosing_scaled.shape
X_test = []
length = len(testData)
timestep = 60

for i in range(timestep, length):
  X_test.append(inputClosing_scaled[i-timestep:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0], X_test.shape[1], 1))
X_test.shape

y_pred = model.predict(X_test)
y_pred

predicted_price = sc.inverse_transform(y_pred)

plt.plot(y_test, color = "black", label = 'Stock Price')
plt.plot(predicted_price, color = "blue", label = 'Predicted Stock Price')
plt.title("Google Stock Price Prediction")
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

