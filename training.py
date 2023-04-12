import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, RocCurveDisplay, confusion_matrix, ConfusionMatrixDisplay, roc_auc_score, recall_score, f1_score
import pickle
import preProc_featExtract


with h5.File('./hdf5_data.h5', 'r') as hdf:
    train = np.array(hdf.get('Dataset/Train/Data'))
    test = np.array(hdf.get('Dataset/Test/Data'))
    trainLabels = np.array(hdf.get('Dataset/Train/Label'))
    testLabels = np.array(hdf.get('Dataset/Test/Label'))
trainFeats = preProc_featExtract.preproc(train)

testFeats = preProc_featExtract.preproc(test)
# clf = LogisticRegression(max_iter=10000)
clf = SVC(probability=True)
clf.fit(trainFeats, trainLabels)
pred = clf.predict(testFeats)
clf_prob = clf.predict_proba(testFeats)
# print(pred, clf_prob)

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

# #calculate the AUC
auc = roc_auc_score(testLabels, clf_prob[:,1])
print('the AUC is: ', auc)

# # Calculate the F1 Score
f1 = f1_score(testLabels, pred)
print('F1 score:', f1)

# # Create a pickle object to save the model
# pickle.dump(clf, open('predictor.sav', 'wb'))