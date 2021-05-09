# Khuyến nghị: học viên nên sử dụng Google Colab

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss

bank = pd.read_csv("bank-full.csv",
                   sep = ";",
                   na_values = "unknown")

#bank.head()

print(bank.shape)
#bank.columns

bank["default"] = bank["default"].map({"no":0,"yes":1})
bank["housing"] = bank["housing"].map({"no":0,"yes":1})
bank["loan"] = bank["loan"].map({"no":0,"yes":1})
bank["y"] = bank["y"].map({"no":0,"yes":1})
bank.education = bank.education.map({"primary": 0, "secondary":1, "tertiary":2})
bank.month = pd.to_datetime(bank.month, format = "%b").dt.month

print(bank.isnull().sum())
print(bank.y.value_counts())

bank.drop(["poutcome", "contact"], axis = 1, inplace = True)
bank.dropna(inplace = True)
bank = pd.get_dummies(bank, drop_first = True)

X = bank.drop("y", axis = 1)
y = bank.y

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, stratify=y)
print("y_train: ", y_train.value_counts())

from sklearn import svm
model = svm.SVC()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

#confusion_matrix(y_test, y_pred)

print("Accuracy: ", accuracy_score(y_test, y_pred))

print("Recall: ", recall_score(y_test, y_pred))

#SMOTE---------------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, stratify=y)

smt = SMOTE()
X_train, y_train = smt.fit_resample(X_train, y_train)
print("y_train: ", y_train.value_counts())
#np.bincount(y_train)

from sklearn import svm
model = svm.SVC()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

#confusion_matrix(y_test, y_pred)

print("Accuracy: ", accuracy_score(y_test, y_pred))

print("Recall: ", recall_score(y_test, y_pred))


#NearMiss--------------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, stratify=y)

nr = NearMiss()
X_train, y_train = nr.fit_resample(X_train, y_train)
print("y_train: ", y_train.value_counts())
#np.bincount(y_train)

from sklearn import svm
model = svm.SVC()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

#confusion_matrix(y_test, y_pred)

print("Accuracy: ", accuracy_score(y_test, y_pred))

print("Recall: ", recall_score(y_test, y_pred))
