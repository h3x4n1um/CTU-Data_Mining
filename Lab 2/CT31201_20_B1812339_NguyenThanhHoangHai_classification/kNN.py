from sklearn import datasets
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier

import numpy as np

def knn(ds):
    model = KNeighborsClassifier()
    for n_fold in range(2, 6):
        scores = model_selection.cross_val_score(model, ds.data, ds.target, cv=n_fold)
        print("Accuracy of model with {}-fold {:.3f}".format(n_fold, np.mean(scores)))

if __name__ == "__main__":
    print("\nbreast cancer wisconsin dataset:")
    knn(datasets.load_breast_cancer())
    print("\nwine dataset:")
    knn(datasets.load_wine())
    print("\ndigits dataset:")
    knn(datasets.load_digits())
