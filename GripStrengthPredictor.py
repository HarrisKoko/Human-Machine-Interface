# Human Machine Interface Villanova Senior Design
# This class builds a predictive model for human grip strength measured by EMG
# https://towardsdatascience.com/linear-regression-with-pytorch-eb6dedead817

# Required Imports for the following machine learning model
import numpy as np
import json
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
from collections import OrderedDict
import tempfile

class GripStrengthPredictor:

    def __init__(self,path):
        pd.set_option('display.max_columns', None)
        self.dataset = self.getDataset(path)


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
        self.dataset = pd.concat(dfs)

    def backwardsPropogation(self):
        inputDim = 1        # takes variable 'x' 
        outputDim = 1       # takes variable 'y'
        learningRate = 0.01 
        epochs = 100

        model = linearRegression(inputDim, outputDim)
        ##### For GPU #######
        if torch.cuda.is_available():
            model.cuda()

        criterion = torch.nn.MSELoss() 
        optimizer = torch.optim.SGD(model.parameters(), lr=learningRate)
        for epoch in range(epochs):
            # Converting inputs and labels to Variable
            if torch.cuda.is_available():
                inputs = Variable(torch.from_numpy(x_train).cuda())
                labels = Variable(torch.from_numpy(y_train).cuda())
            else:
                inputs = Variable(torch.from_numpy(x_train))
                labels = Variable(torch.from_numpy(y_train))

            # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
            optimizer.zero_grad()

            # get output from the model, given the inputs
            outputs = model(inputs)

            # get loss for the predicted output
            loss = criterion(outputs, labels)
            print(loss)
            # get gradients w.r.t to parameters
            loss.backward()

            # update parameters
            optimizer.step()

            print('epoch {}, loss {}'.format(epoch, loss.item()))

    def forwardPropogation(self):
        with torch.no_grad(): # we don't need gradients in the testing phase
            if torch.cuda.is_available():
                predicted = model(Variable(torch.from_numpy(x_train).cuda())).cpu().data.numpy()
            else:
                predicted = model(Variable(torch.from_numpy(x_train))).data.numpy()
            print(predicted)

        plt.clf()
        plt.plot(x_train, y_train, 'go', label='True data', alpha=0.5)
        plt.plot(x_train, predicted, '--', label='Predictions', alpha=0.5)
        plt.legend(loc='best')
        plt.show()

class linearRegression(torch.nn.Module):

        def __init__(self, inputSize, outputSize):
            super(linearRegression, self).__init__()
            self.linear = torch.nn.Linear(inputSize, outputSize)

        def forward(self, x):
            out = self.linear(x)
            return out

def main():
    a = GripStrengthPredictor('Datasets')
    print('Done')

main()