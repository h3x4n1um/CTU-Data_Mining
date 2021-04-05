from sklearn import linear_model

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    x = np.array([[147, 150, 153, 158, 163, 165, 168, 170, 173, 175, 178, 180, 183]]).T
    y = np.array([[49, 50, 51,  54, 58, 59, 60, 62, 63, 64, 66, 67, 68]]).T

    lm = linear_model.LinearRegression()
    lm.fit(x,y)

    x1 = np.array([[145, 185]]).T
    y1 = lm.predict(x1)

    plt.plot(x, y, "ro", color="blue")
    plt.plot(x1, y1, color="violet")
    plt.axis([140, 190, 45, 100])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
