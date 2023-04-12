import h5py as h5
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import recall_score
import preProc_featExtract


with h5.File('./hdf5_data.h5', 'r') as hdf:
    train = np.array(hdf.get('Dataset/Train/Data'))
    test = np.array(hdf.get('Dataset/Test/Data'))
    trainLabels = np.array(hdf.get('Dataset/Train/Label'))
    testLabels = np.array(hdf.get('Dataset/Test/Label'))

# These lists will hold [index, max value]    
maxAcc = [0, 0]
maxRec = [0, 0]
maxAUC = [0, 0]
for i in range(1, 100):
  print(i)
  trainFeats = preProc_featExtract.preproc(train)
  testFeats = preProc_featExtract.preproc(test)
  clf = make_pipeline(LogisticRegression(max_iter=10000))
  clf.fit(trainFeats, trainLabels)
  pred = clf.predict(testFeats)
  clf_prob = clf.predict_proba(testFeats)

  acc = accuracy_score(testLabels, pred)
  recall = recall_score(testLabels, pred)
  #calculate the AUC
  auc = roc_auc_score(testLabels, clf_prob[:,1])
  if(acc > maxAcc[1]):
     maxAcc[0] = i
     maxAcc[1] = acc
  if(auc > maxAUC[1]):
     maxAUC[0] = i
     maxAUC[1] = auc
  if(recall > maxRec[1]):
     maxRec[0] = i
     maxRec[1] = recall
print(maxAcc, maxAUC, maxRec)