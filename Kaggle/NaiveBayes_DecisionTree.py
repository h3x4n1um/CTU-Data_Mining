from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder

import numpy as np
import pandas as pd

def NaiveBayes_fit(x, y) -> dict:
    train_stats = dict({"size": len(x)})
    for label in y.unique():
        label = label.item()

        df_tmp = x[y == label]
        df_tmp = df_tmp.assign(Y = y[y == label])

        train_stats[label] = dict()
        for ft in df_tmp.columns:
            train_stats[label][ft] = df_tmp[ft].value_counts(dropna=False).to_dict()
    return train_stats

def NaiveBayes_predict(x, train_stats: dict) -> list:
    y = list()
    for i in range(len(x)):
        ele = x.iloc[i]
        last_ratio = 0
        res_label = None

        for label in train_stats.keys():
            if label != "size":
                ratio = train_stats[label]['Y'][label]/train_stats["size"]
                for ft in ele.index:
                    ratio = ratio*(train_stats[label][ft][ele[ft]]/train_stats[label]['Y'][label])

                if ratio >= last_ratio:
                    last_ratio = ratio
                    res_label = label
        y.append(res_label)
    return y

if __name__ == "__main__":
    df = pd.read_csv("in-vehicle-coupon-recommendation.csv")

    df.drop('car', axis=1, inplace=True)
    df.dropna(subset=["CarryAway", "RestaurantLessThan20"], inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("category")

    x = df.drop('Y', axis=1)
    y = df['Y']

    oe = OneHotEncoder(sparse=False)
    x = pd.DataFrame(oe.fit_transform(x), index=y.index, columns=oe.get_feature_names())

    loop_cnt = 10
    nb_acc = list()
    dtc_acc = list()

    for cnt in range(loop_cnt):
        x_train, x_test, y_train, y_test = train_test_split(x,
                                                            y,
                                                            test_size=1/3,
                                                            random_state=cnt+100)

        train_stats = NaiveBayes_fit(x_train, y_train)
        nb_y_pred = NaiveBayes_predict(x_test, train_stats)

        dtc = DecisionTreeClassifier(
            max_depth=5,
            min_samples_split=3
        )
        dtc.fit(x_train, y_train)
        dtc_y_pred = dtc.predict(x_test)

        nb_acc.append(accuracy_score(y_test, nb_y_pred))
        dtc_acc.append(accuracy_score(y_test, dtc_y_pred))

        print("cnt: {}".format(cnt))
        print("Naive Bayes:\t{}".format(nb_acc[cnt]))
        print("Decision Tree:\t{}\n".format(dtc_acc[cnt]))


    nb_acc = pd.Series(nb_acc)
    dtc_acc = pd.Series(dtc_acc)
    print("Mean Naive Bayes:\t{}".format(nb_acc.mean()))
    print("Mean Decision Tree:\t{}".format(dtc_acc.mean()))

    print("Max Naive Bayes:\t{}".format(nb_acc.max()))
    print("Max Naive Bayes cnt:\t{}".format(nb_acc.argmax()))

    
