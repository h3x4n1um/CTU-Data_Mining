
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("D:\Code\Python\Data Mining\Kaggle\in-vehicle-coupon-recommendation.csv")

    df.drop('car', axis=1, inplace=True)
    df.dropna(subset=["CarryAway", "RestaurantLessThan20"], inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("category")

    x = df.drop('Y', axis=1)
    y = df['Y']

    oe = OneHotEncoder(sparse=False)
    x = oe.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=7)

    dtc = DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=3,
        random_state=5
    )
    dtc.fit(x_train, y_train)
    y_pred = dtc.predict(x_test)

    print(accuracy_score(y_test, y_pred))
    ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test, y_pred)).plot()
    plt.show()