"""Dataset: https://archive.ics.uci.edu/ml/datasets/bank+marketing"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.rc("font", size=14)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

"""# 1. Đọc dữ liệu"""

data = pd.read_csv('bank-additional-full.csv', header=0, sep=';')
data = data.dropna()
print(data.shape)
print(list(data.columns))

data.head()

print(data["education"].unique())

# Gom các loại hình đào tạo “basic.4y”, “basic.9y” và “basic.6y” thành “basic”.
data['education']=np.where(data['education'] =='basic.9y', 'Basic', data['education'])
data['education']=np.where(data['education'] =='basic.6y', 'Basic', data['education'])
data['education']=np.where(data['education'] =='basic.4y', 'Basic', data['education'])

data["education"].unique()

"""# 2. Phân tích khám phá dữ liệu (Exploratory Data Analysis – EDA)"""

# Xem thành phần giá trị của biến đầu ra (output values)
data['y'].value_counts()

sns.countplot(x='y', data=data, palette='hls')
plt.show()

# Tính theo %
count_no_sub = len(data[data['y']=='no'])
count_sub = len(data[data['y']=='yes'])
pct_of_no_sub = count_no_sub/(count_no_sub+count_sub)
print("percentage of no subscription is", round(pct_of_no_sub*100, 2))
pct_of_sub = count_sub/(count_no_sub+count_sub)
print("percentage of subscription", round(pct_of_sub*100, 2))

"""Chúng ta thấy rằng tập dữ liệu này bị mất cần bằng (tỉ lệ 89:11)"""

# Sử dụng groupby để phân tích đặc điểm dữ liệu
data.groupby('y').mean()
# Bạn nhận xét gì về kết quả. Ví dụ như số tuổi trung bình của nhóm mua hàng đối với nhóm không mua

data.groupby('job').mean()


"""# Hiển thị dữ liệu"""

#Vẽ đồ thị mối quan hệ giữa nghề nghiệp và Tần suất mua hàng
# %matplotlib inline
pd.crosstab(data.job,data.y).plot(kind='bar')
plt.title('Purchase Frequency for Job Title')
plt.xlabel('Job')
plt.ylabel('Frequency of Purchase')
plt.savefig('purchase_fre_job')

"""Qua đồ thị bên trên ta thấy rằng Job có thể là một yếu tố dự báo tốt."""

#Vẽ đồ thị mối quan hệ giữa tình trạng hôn nhân và mua hàng
table=pd.crosstab(data.marital,data.y)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Marital Status vs Purchase')
plt.xlabel('Marital Status')
plt.ylabel('Proportion of Customers')
plt.savefig('mariral_vs_pur_stack')

"""Qua đồ thị bên trên ta thấy rằng Tình trạng hôn nhân dường như không phải là một yếu tố tố dự báo tốt."""


# kết quả của chiến dịch tiếp thị trước đó
pd.crosstab(data.poutcome,data.y).plot(kind='bar')
plt.title('Purchase Frequency for Poutcome')
plt.xlabel('Poutcome')
plt.ylabel('Frequency of Purchase')
plt.savefig('pur_fre_pout_bar')

# Tuổi
data.age.hist()
plt.title('Histogram of Age')
plt.xlabel('Age')
plt.ylabel('Frequency of Purchase')
plt.savefig('hist_age')

# Trình độ học vấn
data.education.hist()
plt.title('Histogram of Education')
plt.xlabel('Education')
plt.ylabel('Frequency of Purchase')
plt.savefig('hist_edu')

# Theo tháng
data.month.hist()
plt.title('Histogram of Month')
plt.xlabel('Month')
plt.ylabel('Frequency of Purchase')
plt.savefig('hist_month')

# Theo ngày
data.day_of_week.hist()
plt.title('Histogram of Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Frequency of Purchase')
plt.savefig('hist_dow')