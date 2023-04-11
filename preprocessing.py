import h5py as h5
import numpy as np
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

with h5.File('./hdf5_data.h5', 'r') as hdf:
    # data = hdf.get('/Dataset/Train')
    data = np.array(hdf.get('Dataset/Train/Data'))
    labels = np.array(hdf.get('Dataset/Train/Label'))

# Prepare a StandardScaler object
sc = preprocessing.StandardScaler()

# Create a df for feature extraction 
features = pd.DataFrame(columns=['min', 'max', 'mean', 'std', 'variance', 'kurtosis', 'skew'])

# Create a np array that is the same size as data that will contain the pre-processed values (don't want to overwrite original data)
pre = np.zeros((data.shape[0], data.shape[1], data.shape[2]))
for c, i in enumerate(data):
  # Create 2D pd df using the values of the window
  df = pd.DataFrame(i, columns=['time', 'x', 'y', 'z', 'absolute'])
  # Apply z-score normalization, this makes the mean 0 and sd 1 for each column
  df = sc.fit_transform(i)
  # Convert np array to pd dataframe
  df = pd.DataFrame(df, columns=['time', 'x', 'y', 'z', 'absolute'])
  # Save pre-processed data to specific dataframe
  pre[c] = df
  df_sma5 = df.rolling(5).mean().dropna()
  


  break
  


