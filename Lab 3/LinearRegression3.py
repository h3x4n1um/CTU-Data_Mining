from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    data = pd.DataFrame(pd.read_csv("https://raw.githubusercontent.com/ltdaovn/dataset/master/advertising.csv"))
    print(data.describe())
    print(data.isnull().sum()*100/data.shape[0])

    fig, axs = plt.subplots(3, figsize = (5,5))
    plt1 = sns.boxplot(data["TV"], ax = axs[0])
    plt2 = sns.boxplot(data["Newspaper"], ax = axs[1])
    plt3 = sns.boxplot(data["Radio"], ax = axs[2])
    plt.tight_layout()

    sns.boxplot(data['Sales'])
    plt.show()

    sns.pairplot(data, x_vars=['TV', 'Newspaper', 'Radio'], y_vars='Sales', height=4, aspect=1, kind='scatter')
    plt.show()

    sns.heatmap(data.corr(), cmap="YlGnBu", annot = True)
    plt.show()

    X = data[['TV']]
    y = data['Sales']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    
    linearreg = LinearRegression()
    linearreg.fit(X_train, y_train)

    y_predict = linearreg.predict(X_test)
    print("Coefficients: ", linearreg.coef_)
    print("Intercept: ", round(linearreg.intercept_,4))
    print("Sales =", round(linearreg.intercept_,4), "+", round(linearreg.coef_[0],4), "× TV")

    print("mean_squared_error: ", np.sqrt(metrics.mean_squared_error(y_test, y_predict)))

    plt.scatter(X_test, y_test)
    plt.plot(X_test, y_predict, color='red', linewidth=3)
    plt.show()
