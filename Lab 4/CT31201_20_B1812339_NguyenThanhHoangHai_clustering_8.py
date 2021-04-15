from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv(
    'https://raw.githubusercontent.com/ltdaovn/dataset/master/ABC_customerSpending.csv',
    index_col=0,
    parse_dates=[4],
    infer_datetime_format=True
)

df_pivot = df.pivot_table(
    index="CUST_ID",
    columns="PRODUCT_CATE",
    values="ORDER_COST",
    aggfunc={'ORDER_COST': np.sum}
).fillna(value=0)

X = df_pivot.values

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

km4 = KMeans(n_clusters=4)
y_means = km4.fit_predict(X)
print(y_means)