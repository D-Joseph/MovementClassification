import pandas as pd
import numpy as np
import preProc_feat_train
import pickle

def inputData(data: str):
  data = pd.read_csv(data)
  result = {0:0, 1:0}
  segments = []
  numSegs = len(data) // 500
  for i in range(numSegs):
    beg = i * 500
    end = beg + 500
    segments.append(data.iloc[beg:end, :]) 
  segments = np.array(segments)
  inputFeats=preProc_feat_train.preproc(segments)
  clf = pickle.load(open('predictor.sav', 'rb'))
  pred = clf.predict(inputFeats)
  clf_prob = clf.predict_proba(inputFeats)
  print(pred)
  for i in pred:
    result[i] += 1
  print(result)
  print(clf_prob)
