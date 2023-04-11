import numpy as np
import pandas as pd
import h5py as h5
from sklearn.model_selection import train_test_split



# This is the smallest csv file, so limit the size of other files to ensure that they all represent similar times
# Round this number down to nearest 500 as we will split into 500 row (~5s) segments
minData = (len(pd.read_csv('Data/DanielWalkingHand.csv')) // 500) * 500

# Create pandas dataframes for each member's data
charWalkingData = pd.concat([
        pd.read_csv('Data/CharWalkingHand.csv', nrows=minData), pd.read_csv('Data/CharWalkingJacket.csv', nrows=minData), pd.read_csv('Data/CharWalkingPant.csv', nrows=minData), 
                          ])
charJumpingData = pd.concat([
        pd.read_csv('Data/NileJumpingHand.csv', nrows=minData), pd.read_csv('Data/NileJumpingJacket.csv', nrows=minData), pd.read_csv('Data/NileJumpingPant.csv', nrows=minData), 
    ])
nileWalkingData = pd.concat([
        pd.read_csv('Data/CharJumpingHand.csv', nrows=minData), pd.read_csv('Data/CharJumpingJacket.csv', nrows=minData), pd.read_csv('Data/CharJumpingPant.csv', nrows=minData), 
                          ])
nileJumpingData = pd.concat([
        pd.read_csv('Data/NileWalkingHand.csv', nrows=minData), pd.read_csv('Data/NileWalkingJacket.csv', nrows=minData), pd.read_csv('Data/NileWalkingPant.csv', nrows=minData), 
])
danJumpingData = pd.concat([
        pd.read_csv('Data/DanielJumpingHand.csv', nrows=minData), pd.read_csv('Data/DanielJumpingJacket.csv', nrows=minData), pd.read_csv('Data/DanielJumpingPant.csv', nrows=minData), 
                          ])
danWalkingData = pd.concat([
        pd.read_csv('Data/DanielWalkingHand.csv', nrows=minData), pd.read_csv('Data/DanielWalkingJacket.csv', nrows=minData), pd.read_csv('Data/DanielWalkingPant.csv', nrows=minData), 
])

# Combine into walking and jumping data
walkingData = pd.concat([charWalkingData, nileWalkingData, danWalkingData])
jumpingData = pd.concat([charJumpingData, nileJumpingData, danJumpingData])
# Label data with 0 or 1 if walking or jumping
walkingData['label'] = 0
jumpingData['label'] = 1
allData = pd.concat([walkingData, jumpingData])

# Split all data into 5 second (~500 rows) windows
numSegs = len(allData) // 500 # Find how many segments there will be

segmentedData = [] # Will hold the 500 record segments
labels = [] # Will hold the classification of each grouping of 500 segments

for i in range(numSegs):
    beg = i * 500
    end = beg + 500
    # In the segments, only include the data and not the final column
    segmentedData.append(allData.iloc[beg:end, :-1]) 
    # Only include the final column, all the segments in 1 window will have the same label so just pull the first one
    labels.append(allData.iloc[beg, -1]) 
segmentedData = np.array(segmentedData)
labels = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(segmentedData, labels, test_size=0.1, shuffle=True, random_state=0)

# Create hdf5 file with subfolders for the train and test data, and each members combined data and raw data
with h5.File('./hdf5_data.h5', 'w') as hdf:
    data = hdf.create_group('/Dataset')
    test = data.create_group('/Dataset/Test')
    test.create_dataset('Data', data=X_test)
    test.create_dataset('Label', data=y_test)
    train = data.create_group('/Dataset/Train')
    train.create_dataset('Data', data=X_train)
    train.create_dataset('Label', data=y_train)

      
    char = hdf.create_group('/Char')
    char.create_dataset('Walking', data=charWalkingData)
    char.create_dataset('walkingPant', data=pd.read_csv('Data/CharWalkingPant.csv'))
    char.create_dataset('Jumping', data=charJumpingData)

    nile = hdf.create_group('/Nile')
    nile.create_dataset('Walking', data=nileWalkingData) 
    nile.create_dataset('Jumping', data=nileJumpingData)

    dan = hdf.create_group('/Dan')
    dan.create_dataset('Walking', data=danWalkingData)
    dan.create_dataset('Jumping', data=danJumpingData)

    comb = hdf.create_group('/Combined')
    comb.create_dataset('Walking', data=walkingData)
    comb.create_dataset('Jumping', data=jumpingData)
    comb.create_dataset('All', data=allData)
    comb.create_dataset('Segmented', data=segmentedData)
    comb.create_dataset('Labels', data=labels)
hdf.close()