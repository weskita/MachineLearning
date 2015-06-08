# -*- coding: utf-8 -*-
"""
Sklear svm example
"""
print(__doc__)


#使用SVM  分类器
from sklearn import svm
from sklearn.datasets import load_svmlight_file
#将数据集分为训练集、检验集
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
#引入评价指标
from sklearn.metrics import confusion_matrix    #计算混淆矩阵
from sklearn.metrics import matthews_corrcoef #计算MCC
from sklearn.metrics import  roc_auc_score  #计算MCC 只对二分类可以计算
from sklearn.metrics import  accuracy_score  #计算ACC

#引入数据
fr_n="/path/your_svm_file"
X,y=load_svmlight_file(fr_n)

# Run classifier  
print("===cross validation===")
clf = svm.SVC(kernel='rbf')
scores=cross_validation.cross_val_score(clf,X,y,cv=5,scoring="accuracy")
print(scores,scores.mean())

print("===performance on TEST===")
# Split the data into a training set and a test set; 分为训练集 检验集
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
clf= svm.SVC(kernel='rbf')
clf.fit(X_train,y_train)
y_pred =clf.predict(X_test)
# 计算混淆 矩阵 Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
#计算准确率,MCC等
print("MCC: %f " %matthews_corrcoef(y_test,y_pred))
print( "ACC:  %f "  %accuracy_score(y_test,y_pred))


print("===compute auc ===")
#compute the auc
classifier = svm.SVC(kernel='rbf',probability=True)
model=classifier.fit(X_train,y_train)
y_prob =classifier.predict_proba(X_test)[:,1] #get the probability of positive
print(y_test)
print(y_prob)
print( "AUC:  %f "  %roc_auc_score(y_test,y_prob))