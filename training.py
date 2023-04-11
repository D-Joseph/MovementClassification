import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import roc_auc_score
from sklearn.metrics import recall_score
import pickle
import preProc_featExtract


with h5.File('./hdf5_data.h5', 'r') as hdf:
    train = np.array(hdf.get('Dataset/Train/Data'))
    test = np.array(hdf.get('Dataset/Test/Data'))
    trainLabels = np.array(hdf.get('Dataset/Train/Label'))
    testLabels = np.array(hdf.get('Dataset/Test/Label'))
trainFeats = preProc_featExtract.preproc(train)
testFeats = preProc_featExtract.preproc(test)
clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=10000))
clf.fit(trainFeats, trainLabels)
pred = clf.predict(testFeats)
clf_prob = clf.predict_proba(testFeats)
print(pred, clf_prob)

acc = accuracy_score(testLabels, pred)
print('accuracy is ', acc)
recall = recall_score(testLabels, pred)
print('recall is: ', recall)


cm = confusion_matrix(testLabels, pred)
cm_display = ConfusionMatrixDisplay(cm).plot()
plt.show()


#plot the ROC curve
fpr, tpr, _= roc_curve(testLabels, clf_prob[:, 1], pos_label=clf.classes_[1])
roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
plt.show()

#calculate the AUC
auc = roc_auc_score(testLabels, clf_prob[:,1])
print('the AUC is: ', auc)

# Create a pickle object to save the model
pickle.dump(clf, open('predictor.sav', 'wb'))