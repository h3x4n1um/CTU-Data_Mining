# Yêu cầu: hãy gom nhóm tập khách hàng sau của công ty bán lẻ ABC dựa trên
# (i) thu nhập hằng năm (Annual Income) và điểm thành viên (Spending Score)

# Ghi chú: học viên cần xem thêm tài liệu của các thư viện để hiểu rõ các thông số của giải thuật

# Nạp các gói thư viện cần thiết
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Chuẩn bị dữ liệu
# Đọc dữ liệu từ tập tin csv
df = pd.read_csv('https://raw.githubusercontent.com/ltdaovn/dataset/master/ABC_Customers.csv')

# Chuẩn hóa tên cột
df.rename(index=str, columns={'Annual Income (k$)': 'Income','Spending Score (1-100)': 'Score'}, inplace=True)

# Lấy dữ liệu thu nhập hằng năm (Annual Income)
# và điểm thành viên (Spending Score) để phân lớp
X = df.loc[:, ('Income', 'Score')]

# 2. Khởi tạo đồ thị
fig = plt.figure(figsize=(20,15))

# 3. Tiến hành gom nhóm

# 3.1. Sử dụng kmeans
from sklearn.cluster import KMeans
km5 = KMeans(n_clusters=5).fit(X)

# Vẽ biểu đồ
X['Labels'] = km5.labels_
ax = fig.add_subplot(221)
sns.scatterplot(X['Income'], X['Score'], hue=X['Labels'],palette=sns.color_palette('hls', 5))
ax.set_title('KMeans with 5 Clusters')

# 3.2. Sử dụng giải thuật Agglomerative Hierarchical Clustering
from sklearn.cluster import AgglomerativeClustering
agglom = AgglomerativeClustering(n_clusters=5, linkage='average').fit(X)

# Vẽ biểu đồ
X['Labels'] = agglom.labels_
ax = fig.add_subplot(222)
sns.scatterplot(X['Income'], X['Score'], hue=X['Labels'],palette=sns.color_palette('hls', 5))
ax.set_title('Agglomerative with 5 Clusters')

# 3.3. Sử dụng giải thuật DBSCAN
from sklearn.cluster import DBSCAN
db = DBSCAN(eps=11, min_samples=6).fit(X)
# Vẽ biểu đồ
ax = fig.add_subplot(223)
X['Labels'] = db.labels_
sns.scatterplot(X['Income'], X['Score'], hue=X['Labels'],palette=sns.color_palette('hls', np.unique(db.labels_).shape[0]))
ax.set_title('DBSCAN with epsilon 11, min samples 6')

# 3.4. Sử dụng giải thuật MeanShift
from sklearn.cluster import MeanShift, estimate_bandwidth
bandwidth = estimate_bandwidth(X, quantile=0.1)
ms = MeanShift(bandwidth).fit(X)
X['Labels'] = ms.labels_
ax = fig.add_subplot(224)
sns.scatterplot(X['Income'], X['Score'], hue=X['Labels'], style=X['Labels'], s=60,palette=sns.color_palette('hls', np.unique(ms.labels_).shape[0]), ax=ax)
ax.set_title('MeanShift')

# 4. Hiển thị đồ thị
plt.tight_layout()
plt.show()