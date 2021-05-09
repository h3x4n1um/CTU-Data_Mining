# %% [markdown]
# # Get input file path

# %% [code] {"jupyter":{"outputs_hidden":false}}
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# %% [markdown]
# # Load and describe

# %% [code] {"jupyter":{"outputs_hidden":false}}
df = pd.read_csv("D:\Code\Python\Data Mining\Kaggle\in-vehicle-coupon-recommendation.csv")
df

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
df[df['Y'] == 0]["destination"].value_counts()

# %%
x = df.drop('Y', axis=1)
y = df['Y']

# %%
x.dtypes

# %%
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=7)

# %%
train_stats = dict()
for val in y_train.unique():
    val = val.item()

    df_tmp = x_train[y_train == val]
    df_tmp = df_tmp.assign(Y = y_train[y_train == val])

    train_stats[val] = dict()
    for col in df_tmp.columns:
        train_stats[val][col] = df_tmp[col].value_counts(dropna=False).to_dict()

# %%
import json
print(json.dumps(train_stats, indent=2))

# %%
train_stats[0]["destination"]["Work"]

# %%
for val in y_train.unique():
    val = val.item()
    print("Y: {}\n\t{}\n\t{}".format(
        val,
        train_stats[val]['Y'][val],
        train_stats[val]['Y'][val]/len(df)
    ))

# %%
import random

i = random.randrange(len(x_test))
ele = x_test.iloc[i]
print(i, ':')
for val in df['Y'].unique():
    val = val.item()
    for id in ele.index:
        print("\t[{} - {} - \"{}\"]:\n\t\t{}\n\t\t{}".format(
            val,
            id,
            ele[id],
            train_stats[val][id][ele[id]],
            train_stats[val][id][ele[id]]/train_stats[val]['Y'][val]
        ))

# %%
y_test

# %%
