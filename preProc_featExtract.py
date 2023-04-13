import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def preproc(data):
  # Prepare a StandardScaler object
  sc = StandardScaler()
  # Create a df for feature extraction and define the desired features
  features = pd.DataFrame(columns=[
    'minX', 'minY', 'minZ', 'minA',
    'maxX', 'maxY', 'maxZ', 'maxA',
    'meanX', 'meanY', 'meanZ', 'meanA',
    'skewX', 'skewY', 'skewZ', 'skewA',
    'stdX', 'stdY', 'stdZ', 'stdA',
    'medianX', 'medianY', 'medianZ', 'medianA',
    'rangeX', 'rangeY', 'rangeZ', 'rangeA',
    'kurtX', 'kurtY', 'kurtZ', 'kurtA',
    'varX', 'varY', 'varZ', 'varA',
    'rmsX', 'rmsY', 'rmsZ', 'rmsA'
    ])
  # Iterate through each window
  for c, i in enumerate(data):
    # Create 2D pd df using the values of the window
    df = pd.DataFrame(i, columns=['time', 'x', 'y', 'z', 'a'])

    # df.mask(df.isin(['-']), other=np.nan, inplace=True) # Change all '-' values to NaNs
    # df = df.astype('float64')
    # df.interpolate(method='linear', inplace=True) # Use linear interpolation to fill missing values

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

    # Plot each column as a line
    # ax[0].plot(df.x, label='x Acceleration')
    # ax[0].plot(df.y, label='y Acceleration')
    # ax[0].plot(df.z, label='z Acceleration')
    # ax[0].plot(df.a, label='Absolute Acceleration')
    # ax[0].set_ylabel('Value')
    # ax[0].set_title("Original Data")
    # ax[0].legend()

    # Apply z-score normalization, this makes the mean 0 and sd 1 for each column
    df = sc.fit_transform(i)
    # Convert np array to pd dataframe to use rolling and for plotting
    df_norm = pd.DataFrame(df, columns=['time', 'x', 'y', 'z', 'a'])

    # Plot data after normalization
    # ax[1].plot(df_norm.x, label='x Acceleration')
    # ax[1].plot(df_norm.y, label='y Acceleration')
    # ax[1].plot(df_norm.z, label='z Acceleration')
    # ax[1].plot(df_norm.a, label='Absolute Acceleration')
    # ax[1].set_ylabel('Value')
    # ax[1].set_title("Normalized Data")
    # ax[1].legend()
    # plt.show()

    # Perform the SMA
    df_sma = df_norm.rolling(26).mean().dropna()

    # # Create a new row for the rolling window statistics
    row = pd.DataFrame({
        'minX': df_sma.x.min(),
        'minY': df_sma.y.min(),
        'minZ': df_sma.z.min(),
        'minA': df_sma.a.min(),

        'maxX': df_sma.x.max(),
        'maxY': df_sma.y.max(),
        'maxZ': df_sma.z.max(),
        'maxA': df_sma.a.max(),

        'meanX': df_sma.x.mean(),
        'meanY': df_sma.y.mean(),
        'meanZ': df_sma.z.mean(),
        'meanA': df_sma.a.mean(),

        'skewX': df_sma.x.skew(),
        'skewY': df_sma.y.skew(),
        'skewZ': df_sma.z.skew(),
        'skewA': df_sma.a.skew(),

        'stdX': df_sma.x.std(),
        'stdY': df_sma.y.std(),
        'stdZ': df_sma.z.std(),
        'stdA': df_sma.a.std(),

        'medianX': df_sma.x.median(),
        'medianY': df_sma.y.median(),
        'medianZ': df_sma.z.median(),
        'medianA': df_sma.a.median(),

        'rangeX': df_sma.x.max() - df_sma.x.min(),
        'rangeY': df_sma.y.max() - df_sma.y.min(),
        'rangeZ': df_sma.z.max() - df_sma.z.min(),
        'rangeA': df_sma.a.max() - df_sma.a.min(),
        
        'kurtX':  df_sma.x.kurt(),
        'kurtY':  df_sma.y.kurt(),
        'kurtZ':  df_sma.z.kurt(),
        'kurtA':  df_sma.a.kurt(),

        'varX': df_sma.x.var(),
        'varY': df_sma.y.var(),
        'varZ': df_sma.z.var(),
        'varA': df_sma.a.var(),

        'rmsX': np.sqrt(np.mean(df_sma.x**2)),
        'rmsY': np.sqrt(np.mean(df_sma.y**2)),
        'rmsZ': np.sqrt(np.mean(df_sma.z**2)),
        'rmsA': np.sqrt(np.mean(df_sma.a**2))
    }, index=[c])
    # Concatenate the new row to the features dataframe
    features = pd.concat([features, row])
  return features