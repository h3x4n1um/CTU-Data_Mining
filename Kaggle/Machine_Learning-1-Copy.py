# %% [markdown]
# # Get input file path

# %% [code] {"jupyter":{"outputs_hidden":false}}
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# %% [markdown]
# # Load and describe

# %% [code] {"jupyter":{"outputs_hidden":false}}
df = pd.read_csv("D:\Code\Python\Data Mining\Kaggle\in-vehicle-coupon-recommendation.csv")
x = df.drop('Y', axis=1)
y = df['Y']
########################Huan luyen tập train
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=7)
x_train=pd.DataFrame(x_train)
y_train=pd.DataFrame(y_train)
df=x_train
df['Y']=y_train
# %% [markdown]
# # Preprocessing dataset

# %% [markdown]
# ## Check for NaN

# %% [code] {"jupyter":{"outputs_hidden":false}}
df_na_sum = df.isna().sum()
df_na_sum[df_na_sum > 0]/len(df)

# %% [markdown]
# ## Drop `car` column since it has 99% `NaN`

# %% [code] {"jupyter":{"outputs_hidden":false}}
df.drop('car', axis=1, inplace=True)
df

# %% [markdown]
# ## Drop `NaN` in `CarryAway` and `RestaurantLessThan20` since it doesn't allow `NaN` and it takes small percent of dataset

# %% [code] {"jupyter":{"outputs_hidden":false}}
df.dropna(subset=["CarryAway", "RestaurantLessThan20"], inplace=True)
df

# %% [markdown]
# ## Change all **object** columns to **category**

# %% [code] {"jupyter":{"outputs_hidden":false}}
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("category")
df

# %% [markdown]
# ## Check if dataset is balanced

# %% [code] {"jupyter":{"outputs_hidden":false}}
df["Y"].value_counts(normalize=True)

# %%
df["Y"].value_counts()

# %%
df_stats = dict()
for val in df['Y'].unique():
    val = val.item()
    df_tmp = df[df['Y'] == val]
    df_stats[val] = dict()
    for col in df_tmp.columns:
        df_stats[val][col] = df_tmp[col].value_counts(dropna=False).to_dict()
import json
print("_______________________SO2")

print(json.dumps(df_stats, indent=2))
# %%
df[df['Y'] == 0]["destination"].value_counts()

# %%
df_stats[0]["destination"]["Work"]
print("_______________________SO3")
# %%
for val in df['Y'].unique():
    val = val.item()
    print("Y: {}\n\t{}\n\t{}".format(
        val,
        df_stats[val]['Y'][val],
        df_stats[val]['Y'][val]/len(df)
    )) 
print("-----------------------------------------------------------")
# %%


import random
print("_______________________SO4")
x_test=df.iloc[:,0:24]
i = random.randrange(len(x_test))
ele = x_test.iloc[i]

#%%Bayes
###########################################################

# tinh xs
print("______________________so5")
def bayesNV(y):
    P_y={}
    for id in ele.index:
        for x in df_stats[y][id]:
            P_y["-".join([str(y),str(id),str(x)])]=df_stats[y][id][x]/df_stats[y]['Y'][y]
    return P_y

def predict():	
	y_predict=list(y_test)
	a1=[]#tt
	a2=[]#gtr
	P_x_y=bayesNV(1)#xs cac gia tri lop 1
	P_x_n=bayesNV(0)#xs cac gia tri lop 0
	P_y_y=df_stats[1]['Y'][1]/len(df) #xs lop 1
	P_y_n=df_stats[0]['Y'][0]/len(df)#xs lop 0
	col=x_test.shape[1]
	row=x_test.shape[0]
	a1=list(x_test[:0])#tt
	for i in range(len(y_test)):
		a2=x_test.iloc[i]
		# tinh xs lop 1
		yes=1
		no=1
		for k in range(0,col):		
			#(str(a1[k]),str(a2[k]))
			yes=P_x_y["-".join(["1",str(a1[k]),str(a2[k])])]
			yes*=yes
			#print(yes)
			no=P_x_n["-".join(["0",str(a1[k]),str(a2[k])])]
			no*=no
		#print("---------------")
		yes=yes*P_y_y
		no=no*P_y_n
		P_y=yes/(yes+no)
		P_n=no/(yes+no)		
		if P_y>P_n:
			y_predict[i]=1
		else:
		 	y_predict[i]=0		
		#print(yes)"""
	return y_predict		
#print(P_1)
#print(P_0)
print("______________________so6")

"""for val in df['Y'].unique():
    val = val.item()
    for id in ele.index:
        for x in df_stats[val][id]:
            print("\t[{} - {} - \"{}\"]:\n\t\t{}\n\t\t{}".format(
                val,
                id,
                x,
                df_stats[val][id][x],
                df_stats[val][id][x]/df_stats[val]['Y'][val]
        ))"""
#print(x_test)
y=predict()
print(y)
#print("do chinh xac:", accuracy_score(y_test,y))
#cnf_matrix_gnb = confusion_matrix(y_test, y)
#print(cnf_matrix_gnb)
