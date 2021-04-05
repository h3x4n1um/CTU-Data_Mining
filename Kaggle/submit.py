# %% [markdown]
# # Get input file path

# %% [code] {"scrolled":false}
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [markdown]
# # Load and describe

# %% [code] {"scrolled":false}
df = pd.read_csv("../input/invehicle-coupon-recommendation/in-vehicle-coupon-recommendation.csv")
df

# %% [code] {"scrolled":false}
df.describe()

# %% [markdown]
# # Preprocessing dataset

# %% [markdown]
# ## Check for NaN

# %% [code] {"scrolled":false}
df.isna().sum()

# %% [code] {"scrolled":false}
df.isna().sum()/len(df)

# %% [markdown]
# ## Drop `car` column since it has 99% NaN

# %% [code] {"scrolled":false}
df = df.drop(['car'], axis=1)
df

# %% [markdown]
# ## Assume `NaN` is `never` in `CarryAway` and `RestaurantLessThan20`
# (Since `CoffeeHouse` and `Restaurant20To50` allow `NaN` value

# %% [code] {"scrolled":false}
df = df.fillna(value={"CarryAway": "never", "RestaurantLessThan20": "never"})
df

# %% [markdown]
# # Value encoding

# %% [code] {"scrolled":false}
dummies_df = pd.get_dummies(df)
dummies_df

# %% [markdown]
# # Split data for train and test (holdout)

# %% [code] {"scrolled":false}
x = dummies_df.drop(['Y'], axis=1)
y = dummies_df['Y']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# %% [markdown]
# ## Train dataset

# %% [code] {"scrolled":false}
x_train

# %% [code] {"scrolled":false}
y_train

# %% [markdown]
# ## Test dataset

# %% [code] {"scrolled":false}
x_test

# %% [code] {"scrolled":false}
y_test

# %% [markdown]
# # Decision Tree classifier

# %% [markdown]
# # Building tree

# %% [code] {"scrolled":false}
from sklearn import tree

dtc = tree.DecisionTreeClassifier(
    max_depth=11,
    min_samples_leaf=3
)
dtc.fit(x_train, y_train)

# %% [markdown]
# ## Validation

# %% [code] {"scrolled":false}
y_pred = dtc.predict(x_test)
y_pred

# %% [code] {"scrolled":false}
from sklearn import metrics

metrics.accuracy_score(y_test, y_pred)

# %% [code] {"scrolled":false}
import matplotlib.pyplot as plt

metrics.plot_confusion_matrix(dtc, x_test, y_test)
plt.show()

# %% [markdown]
# # Naive Bayes classifier

# %% [markdown]
# ## Building model

# %% [code] {"scrolled":false}
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(x_train, y_train)

# %% [markdown]
# ## Validation

# %% [code] {"scrolled":false}
y_pred = gnb.predict(x_test)
y_pred

# %% [code] {"scrolled":false}
metrics.accuracy_score(y_test, y_pred)

# %% [code] {"scrolled":false}
metrics.plot_confusion_matrix(gnb, x_test, y_test)
plt.show()

# %% [markdown]
# # k-Nearest Neighbors

# %% [markdown]
# # Building model

# %% [code]
from sklearn.neighbors import KNeighborsClassifier

knnc = KNeighborsClassifier()
knnc.fit(x_train, y_train)

# %% [markdown]
# # Validation

# %% [code]
y_pred = knnc.predict(x_test)
y_pred

# %% [code]
metrics.accuracy_score(y_test, y_pred)

# %% [code]
metrics.plot_confusion_matrix(knnc, x_test, y_test)
plt.show()

# %% [markdown]
# # Conclusion
# According to the accuracy of 3 models, Decision Tree perform better than Naive Bayes and k-NN