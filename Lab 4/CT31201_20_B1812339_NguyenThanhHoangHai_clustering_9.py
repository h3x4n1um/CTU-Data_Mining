from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("https://raw.githubusercontent.com/ltdaovn/dataset/master/flowers.csv")

X = df.values

clusters = []
for i in range(1, 10):
    km = KMeans(n_clusters=i).fit(X)
    clusters.append(km.inertia_)

fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(
    x=list(range(1, 10)),
    y=clusters,
    ax=ax
)
ax.set_title('Đồ thị Elbow')
ax.set_xlabel('Số lượng nhóm')
ax.set_ylabel('Giá trị Inertia')
plt.show()
plt.cla()

# Qua đồ thị trên, chúng ta thấy số lượng cluster thích hợp là từ 2 đến 3 clusters

# Phân tích dữ liệu được gom thành 3 nhóm
km3 = KMeans(n_clusters=3)
y_means = km3.fit_predict(X)
#print(y_means)

plt.scatter(
    X[y_means == 0, 0],
    X[y_means == 0, 1],
    s=100,
    c='pink',
    label='Nhóm 1'
)
plt.scatter(
    X[y_means == 1, 0],
    X[y_means == 1, 1],
    s=100,
    c='yellow',
    label='Nhóm 2'
)
plt.scatter(
    X[y_means == 2, 0],
    X[y_means == 2, 1],
    s=100,
    c='cyan',
    label='Nhóm 3'
)
plt.scatter(
    km3.cluster_centers_[:, 0],
    km3.cluster_centers_[:, 1],
    s=100,
    c='blue',
    label='Centeroid'
)

plt.style.use('fivethirtyeight')
plt.title('K Means Clustering', fontsize = 20)
plt.xlabel('SepalLength')
plt.ylabel('SepalWidth')
plt.legend()
plt.grid()
plt.show()