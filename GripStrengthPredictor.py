# Human Machine Interface Villanova Senior Design
# This class builds a predictive model for human grip strength measured by EMG
# https://towardsdatascience.com/linear-regression-with-pytorch-eb6dedead817

# Required Imports for the following machine learning model
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import tensorflow as tf
import sklearn.model_selection as sk
import torch.optim as optim
import torch.nn.functional as F
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import sklearn.metrics as s
from math import sqrt
import scipy.io as sio
import os
from torch.autograd import Variable

class GripStrengthPredictor:

    def __init__(self,path):
        pd.set_option('display.max_columns', None)
        self.dataset = self.getDataset(path)
        self.splitData()
        self.backwardsPropogation()

    def getDataset(self,path):
        # Import EMG dataset from Matlab as CSV file
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
        return pd.concat(dfs)

    def splitData(self, train_percent = 0.8):
        x = self.dataset[0]
        y = self.dataset[1]
        # Use int for random_state to make reproducable test/train data. Otherwise, leave null.
        self.x_train, self.x_test, self.y_train, self.y_test = sk.train_test_split( x, y, test_size=1-train_percent, random_state=42) 
        self.x_train = self.x_train.to_numpy()
        assert not np.any(np.isnan(self.x_train))
        self.x_test = self.x_test.to_numpy()
        assert not np.any(np.isnan(self.x_test))
        self.y_train = self.y_train.to_numpy()
        assert not np.any(np.isnan(self.y_train))
        self.y_test = self.y_test.to_numpy()
        assert not np.any(np.isnan(self.y_test))

        self.x_train = torch.from_numpy(self.x_train.astype(np.float32))
        self.x_test = torch.from_numpy(self.x_test.astype(np.float32))
        self.y_train = torch.from_numpy(self.y_train.astype(np.float32))
        self.y_test = torch.from_numpy(self.y_test.astype(np.float32))

    def backwardsPropogation(self):
        self.model = nn.Linear(482917,1)
        learningRate = 0.001 
        epochs = 100
        ##### For GPU #######
        # if torch.cuda.is_available():
        #     self.model.cuda()

        self.criterion = torch.nn.MSELoss() 
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=learningRate)
        for epoch in range(epochs):
            y_pred = self.model(self.x_train)
            loss = self.criterion(y_pred,self.y_train)

            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()

            if((epoch+1)%10 == 0):
                print(f'epoch: {epoch+1}, loss = {loss.item():.4f}')
  
    def forwardPropogation(self):
        # with torch.no_grad(): # we don't need gradients in the testing phase
        #     if torch.cuda.is_available():
        #         self.predicted = self.model(Variable(torch.from_numpy(self.x_test.numpy()).cuda())).cpu().data.numpy()
        #     else:
        self.predicted = self.model(self.x_test)
        print(self.predicted)

        plt.clf()
        plt.plot(self.x_train, self.y_train, 'go', label='True data', alpha=0.5)
        plt.plot(self.x_train, self.predicted, '--', label='Predictions', alpha=0.5)
        plt.legend(loc='best')
        plt.show()
        return self.predicted

class linearRegression(torch.nn.Module):

        def __init__(self, inputSize, outputSize):
            super(linearRegression, self).__init__()
            self.linear = torch.nn.Linear(inputSize, outputSize)

        def forward(self, x):
            out = self.linear(x)
            return out

def main():
    a = GripStrengthPredictor('MuscleTrainingData')
    a.forwardPropogation()
    print('Done')

main()