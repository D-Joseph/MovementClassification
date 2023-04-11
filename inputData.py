import pandas as pd
import numpy as np
import preProc_feat_train
import pickle

def proc(data: str):
  # Convert input csv to pd df
  dataCSV = pd.read_csv(data)

  # Keep track of predictions
  result = {0:0, 1:0}

  # Split into 5s windows
  segments = []
  numSegs = len(dataCSV) // 500
  for i in range(numSegs):
    beg = i * 500
    end = beg + 500
    segments.append(dataCSV.iloc[beg:end, :]) 
  segments = np.array(segments)
  # Feature extraction for inputted data
  inputFeats=preProc_feat_train.preproc(segments)

  # Call model
  clf = pickle.load(open('predictor.sav', 'rb'))
  pred = clf.predict(inputFeats)
  clf_prob = clf.predict_proba(inputFeats)
  print(segments)
  # Output results
  print(pred)
  for i in pred:
    result[i] += 1
  print(result)
  print(clf_prob)

  return ['Walking' if result[0] > result[1] else 'Jumping', dataCSV]
proc('Raw_Data.csv')