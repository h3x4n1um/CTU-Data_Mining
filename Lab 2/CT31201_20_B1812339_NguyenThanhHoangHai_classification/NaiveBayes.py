from sklearn import datasets
from sklearn import metrics
from sklearn import model_selection
from sklearn.naive_bayes import GaussianNB

import matplotlib.pyplot as plt

def naive_bayes(ds):
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        ds.data,
        ds.target,
        test_size=0.3,
        random_state = 7)

    model = GaussianNB()
    model.fit(x_train, y_train)

    metrics.plot_confusion_matrix(model, x_test, y_test)
    plt.show()


if __name__ == "__main__":
    print("\nbreast cancer wisconsin dataset:")
    naive_bayes(datasets.load_breast_cancer())
    print("\nwine dataset:")
    naive_bayes(datasets.load_wine())
    print("\ndigits dataset:")
    naive_bayes(datasets.load_digits())
