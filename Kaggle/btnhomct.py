import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


df = pd.read_csv("D:\Code\Python\Data Mining\Kaggle\in-vehicle-coupon-recommendation.csv")
x= df.iloc[:,0:25]
y= df.Y

def GaussianNB(x,y,dt):
	df=dt
	df2 = dt.dropna()#xài bien tạm , xóa các hàng rỗng
	tam=x.shape
	row=tam[0] # hàng
	col=tam[1] # cột
	#lấy các gia trị của thuộc tính
	value_lable={}
	i=0
	j=0
	for i in range(0,col):
		value_lable[df2.columns[i]]=df2.loc[:,df2.columns[i]].values
		value_lable[df2.columns[i]]=set(value_lable[df2.columns[i]]) # lay cac gia tri cua nhan khong trung lap	# lỗi thiếu giá trị 
		value_lable[df2.columns[i]]=list(value_lable[df2.columns[i]])
	#################################################################
	#dem so phan tu 
	#print(value_lable)
	count_vl={} #count value

	for i in range(0,col) :
		count_vl[df.columns[i]]=df.loc[:,[df.columns[i],"Y"]].value_counts()#dem so phan tu cua tung gia tri/thuộc tính
		#print(df.loc[:,[df.columns[i],"Y"]].value_counts())
	count_vl_y={}#so phan tu co nhan = y = 1||0 // 
	P_y={}#xs gia tri mang lable =1
	sum_all_y={} #mau so y =1||0
	sum1=0
	for i in range(0,col):
		m =len(value_lable[df.columns[i]])#so luong gia tri cua thuộc tính
		sum_all_y[df.columns[i]]=0
		for j in range(0,m):
			sum1+=count_vl[df.columns[i]][value_lable[df.columns[i]][j]][y]#tinh tong gia tri y là 1 hoặc y là 0
		sum_all_y[df.columns[i]]+=sum1 
		sum1=0	
		#print(df.columns[i],sum_all_y[df.columns[i]])
	###############################################################################
	for i in range(0,col):
		m =len(value_lable[df.columns[i]])#so luong gia tri cua thuộc tính
		for j in range(0,m):
			#print("so1")
			#print(df.columns[i])
			#print("so2")
			#print(str(value_lable[df.columns[i]][j]))
			#print("so3")
			#print(count_vl[df.columns[i]][value_lable[df.columns[i]][j]])
			a=str(df.columns[i]) #thuộc tính
			b=str(value_lable[df.columns[i]][j]) #gia tri cua thuộc tính
			count_vl_y["|".join([a,b])]=count_vl[df.columns[i]][value_lable[df.columns[i]][j]][y]
			P_y["|".join([a,b])]=count_vl[df.columns[i]][value_lable[df.columns[i]][j]][y]/sum_all_y[df.columns[i]] #tinh xs , so luong cua gia tri co nhan y=1||0 /tong y =1 hoac 0 
			#print("countvly")
			#print(count_vl_y)
			#count_vl_y["weather"]=count_vl_y[weather][rainy][1]
	print("--------------------------------y:",y)
	print(count_vl_y)		
	return P_y # y=0,1

import json

P_y=GaussianNB(x,1,df)
print("---------------Py")
print(json.dumps(P_y, indent=2))
P_n=GaussianNB(x,0,df)
print("---------------Pn")
print(json.dumps(P_n, indent=2))

