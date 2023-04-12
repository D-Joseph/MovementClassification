import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

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

  for c, i in enumerate(data):
    # Create 2D pd df using the values of the window
    df = pd.DataFrame(i, columns=['time', 'x', 'y', 'z', 'a'])
    # Apply z-score normalization, this makes the mean 0 and sd 1 for each column
    df = sc.fit_transform(i)
    # Convert np array to pd dataframe
    df = pd.DataFrame(df, columns=['time', 'x', 'y', 'z', 'a'])
    df_sma5 = df.rolling(26).mean().dropna()
    # Create a new row for the rolling window statistics
    row = pd.DataFrame({
        'minX': df_sma5.x.min(),
        'minY': df_sma5.y.min(),
        'minZ': df_sma5.z.min(),
        'minA': df_sma5.a.min(),

        'maxX': df_sma5.x.max(),
        'maxY': df_sma5.y.max(),
        'maxZ': df_sma5.z.max(),
        'maxA': df_sma5.a.max(),

        'meanX': df_sma5.x.mean(),
        'meanY': df_sma5.y.mean(),
        'meanZ': df_sma5.z.mean(),
        'meanA': df_sma5.a.mean(),

        'skewX': df_sma5.x.skew(),
        'skewY': df_sma5.y.skew(),
        'skewZ': df_sma5.z.skew(),
        'skewA': df_sma5.a.skew(),

        'stdX': df_sma5.x.std(),
        'stdY': df_sma5.y.std(),
        'stdZ': df_sma5.z.std(),
        'stdA': df_sma5.a.std(),

        'medianX': df_sma5.x.median(),
        'medianY': df_sma5.y.median(),
        'medianZ': df_sma5.z.median(),
        'medianA': df_sma5.a.median(),

        'rangeX': df_sma5.x.max() - df_sma5.x.min(),
        'rangeY': df_sma5.y.max() - df_sma5.y.min(),
        'rangeZ': df_sma5.z.max() - df_sma5.z.min(),
        'rangeA': df_sma5.a.max() - df_sma5.a.min(),
        
        'kurtX':  df_sma5.x.kurt(),
        'kurtY':  df_sma5.y.kurt(),
        'kurtZ':  df_sma5.z.kurt(),
        'kurtA':  df_sma5.a.kurt(),

        'varX': df_sma5.x.var(),
        'varY': df_sma5.y.var(),
        'varZ': df_sma5.z.var(),
        'varA': df_sma5.a.var(),

        'rmsX': np.sqrt(np.mean(df_sma5.x**2)),
        'rmsY': np.sqrt(np.mean(df_sma5.y**2)),
        'rmsZ': np.sqrt(np.mean(df_sma5.z**2)),
        'rmsA': np.sqrt(np.mean(df_sma5.z**2))
    }, index=[c])
    # Concatenate the new row to the features dataframe
    features = pd.concat([features, row], ignore_index=False)
  return features