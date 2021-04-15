# Yêu cầu: hãy gom nhóm tập khách hàng sau của công ty bán lẻ ABC dựa trên
# (i) thu nhập hằng năm (Annual Income) và
# (ii) điểm thành viên (Spending Score)

# Nạp các gói thư viện cần thiết
import pandas as pd

# 1. Chuẩn bị dữ liệu
# Đọc dữ liệu từtập tin csv
df = pd.read_csv('https://raw.githubusercontent.com/ltdaovn/dataset/master/ABC_Customers.csv')

# Lấy dữ liệu thu nhập hằng năm (Annual Income)
# và điểm thành viên (Spending Score) để phân lớp
X = df.iloc[:, [3, 4]].values

# 2. Tiến hành gom nhóm
# Khi sử dụng kmeans để gom nhóm, câu hỏi đặt ra là với dataset đã có,
# chúng ta sẽ phân thành bao nhiêu cụm là hợp lý (tối ưu)?
# Trong ví dụ này chúng ta sẽ sử dụng phương pháp Elbow để xác định số cụm k.
# Tài liệu tham khảo phương pháp Elbow
# https://en.wikipedia.org/wiki/Determining_the_number_of_clusters_in_a_data_set

# Chạy thuật toán KMeans với k=(1, 10)

from sklearn.cluster import KMeans
clusters = []
for i in range(1, 10):
    km = KMeans(n_clusters=i).fit(X)
    clusters.append(km.inertia_)

import matplotlib.pyplot as plt
import seaborn as sns
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

# Qua đồ thị trên, chúng ta thấy số lượng cluster thích hợp là từ 3 đến 5 clusters

# Phân tích dữ liệu được gom thành 5 nhóm
km5 = KMeans(n_clusters=5)
y_means = km5.fit_predict(X)
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
    X[y_means == 3, 0],
    X[y_means == 3, 1],
    s=100,
    c='green',
    label='Nhóm 4'
)
plt.scatter(
    X[y_means == 4, 0],
    X[y_means == 4, 1],
    s=100,
    c='black',
    label='Nhóm 5'
)
plt.scatter(
    km5.cluster_centers_[:,0],
    km5.cluster_centers_[:, 1],
    s=100,
    c='blue',
    label='Centeroid'
)

plt.style.use('fivethirtyeight')
plt.title('K Means Clustering', fontsize = 20)
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
plt.legend()
plt.grid()
plt.show()