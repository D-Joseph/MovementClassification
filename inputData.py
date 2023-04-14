import pandas as pd
import numpy as np
import preProc_featExtract
import pickle

def proc(dataPD):
  # Keep track of predictions
  result = {0:0, 1:0}

  # Split into 5s windows
  segments = []
  numSegs = len(dataPD) // 500
  for i in range(numSegs):
    beg = i * 500
    end = beg + 500
    segments.append(dataPD.iloc[beg:end, :]) 
  segments = np.array(segments)
  # Feature extraction for inputted data
  inputFeats=preProc_featExtract.preproc(segments)

  # Call model
  clf = pickle.load(open('predictor.sav', 'rb'))
  pred = clf.predict(inputFeats)
  clf_prob = clf.predict_proba(inputFeats)

  # Convert the prediction list to a list that has 500 occurences of each element of the original list
  # This is to add a prediction to each row within the window, instead of having 1 prediction per window
  predArr = [x for list in [500 * ['Walking' if i == 0  else 'Jumping'] for i in pred] for x in list]
  
  # Remove all rows that did not fall within a window (i.e. if the input has 501 rows, cut off the last row)
  dataPD = dataPD.iloc[:numSegs * 500, :]
  
  # Output results
  dataPD['Label'] = predArr
  for i in pred:
    result[i] += 1
  print(f'Prediction Array: {pred}\nPrediction Amount: {result}\nclf_prob: {clf_prob}')
  return ['Walking' if result[0] > result[1] else 'Jumping', dataPD]
