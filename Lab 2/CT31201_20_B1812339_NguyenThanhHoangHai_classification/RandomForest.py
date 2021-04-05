from sklearn import datasets
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def bagging(ds):
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        ds.data,
        ds.target,
        test_size=0.3,
        random_state=7
    )

    model = RandomForestClassifier(
        random_state=5
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    print("Accuracy of model with hold-out {:.3f}".format(accuracy_score(y_test, y_pred)))

    feature_importances = pd.Series(
        model.feature_importances_,
        index=ds.feature_names).sort_values(ascending=False)
    
    sns.barplot(x=feature_importances, y=feature_importances.index)

    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title("Visualizing Important Features")
    plt.show()

if __name__ == "__main__":
    print("\nbreast cancer wisconsin dataset:")
    bagging(datasets.load_breast_cancer())
    print("\nwine dataset:")
    bagging(datasets.load_wine())
    print("\ndigits dataset:")
    bagging(datasets.load_digits())
