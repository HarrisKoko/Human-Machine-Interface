import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import tensorflow as tf
import os
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sklearn.model_selection as sk
import sklearn.metrics as skm
from math import sqrt
from sklearn.preprocessing import MinMaxScaler

class LinearRegressionModel(torch.nn.Module):

    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(111628, 1)  # One in and one out
 
    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

class GripStrengthPrediction:

    def getData(self,path):
        dfs = []
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            # checking if it is a file
            if os.path.isfile(f):
                print('Loading file: ',f)
                mat_file = sio.loadmat(f)
                last_entry = list(mat_file) [-1]
                df = pd.DataFrame(mat_file[last_entry])
                dfs.append(df.drop(columns=2))
        data = pd.concat(dfs)
        data = data.to_numpy()
        X = data[:,0]
        y = X = data[:,1]
        # plt.clf()
        # plt.plot(X,y, 'go', label='True data', alpha=0.5)
        # plt.legend(loc='best')
        #plt.show()

        X_train, X_test, y_train, y_test = sk.train_test_split( X, y, test_size=0.3, random_state=23) 
        X_train = np.array(X_train).reshape(-1,1)
        X_test = np.array(X_test).reshape(-1,1)
        return X_train,X_test,y_train,y_test
        

    def getFit(self,X_train,X_test,y_train,y_test):
        lr = LinearRegression()
        lr.fit(X_train,y_train)

        c = lr.intercept_
        m = lr.coef_

        print(m)
        print(c)

        predictions = m*X_test+c
        
        plt.clf()
        plt.plot(X_test, y_test, 'go', label='True Force', alpha=0.5)
        plt.plot(X_test, predictions, '--', label='Force Predictions', alpha=0.5)
        plt.xlabel("EMG Data")
        plt.ylabel("Force")
        plt.legend(loc='best')
        plt.show()

        print("Mean Absolute Error: ",skm.mean_absolute_error(y_test,predictions))
        print("Mean Absolute Error: ",skm.mean_absolute_percentage_error(y_test,predictions))
        print("Mean Absolute Error: ",skm.mean_squared_error(y_test,predictions))
        print("Mean Absolute Error: ",sqrt(skm.mean_squared_error(y_test,predictions)))
        return predictions

    def armPercentile(self,predictions):
        print(predictions)
        scaler = MinMaxScaler(feature_range = (-1,1))
        percentiles = scaler.fit_transform(predictions) 
        print(percentiles)
        return percentiles

def main():
    predictor = GripStrengthPrediction()
    X_train,X_test,y_train,y_test = predictor.getData("MuscleTrainingData")
    predictions = predictor.getFit(X_train,X_test,y_train,y_test)
    armMovements = predictor.armPercentile(predictions)
    
main()