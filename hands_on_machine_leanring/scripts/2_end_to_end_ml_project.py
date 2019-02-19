#! /usr/bin/env python
# -*- coding: utf-8 -*ﬁ-
"""
 @FileName: 2_end_to_end_ml_project
 @Desc:  
 @Author: yuzhongchun
 @Date: 2019-02-19 10:21
 @Last Modified by: yuzhongchun
 @Last Modified time: 2019-02-19 10:21
"""

# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Setup
# Common imports
import numpy as np
import os

# to make this notebook's output stable across runs
np.random.seed(42)

# To plot pretty figures
# % matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "end_to_end_project"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure: ", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


# Ignore useless warnings (see SciPy issue #5998)
import warnings

warnings.filterwarnings(action="ignore", message="^internal gelsd")

# Get the data
import os
import tarfile
from six.moves import urllib

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()


# fetch_housing_data()

import pandas as pd

# True就是可以换行显示。设置成False的时候不允许换行
pd.set_option('expand_frame_repr', False)
# 显示的最大行数和列数，如果超额就显示省略号，这个指的是多少个dataFrame的列。如果比较多又不允许换行，就会显得很乱
pd.set_option('display.max_rows', 10)
# 显示小数点后的位数
# pd.set_option('precision', 5)
# 列长度
pd.set_option('max_colwidth', 20)
# 显示居中还是左边
pd.set_option('colheader_justify', 'left')
# 横向最多显示多少个字符， 一般80不适合横向的屏幕，平时多用200
pd.set_option('display.width', 200)


def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


housing = load_housing_data()
print('===============================================================================================================')
print(housing.head(10))
print('===============================================================================================================')
print(housing.info())
print('===============================================================================================================')
print(housing["ocean_proximity"].value_counts())
print('===============================================================================================================')
print(housing.describe())
print('===============================================================================================================')

import matplotlib.pyplot as plt

housing.hist(bins=50, figsize=(20, 15))
save_fig("attribute_histogram_plots")
plt.show()

# to make this notebook's output identical at every run
np.random.seed(42)


# For illustration only. Sklearn has train_test_split()
def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


train_set, test_set = split_train_test(housing, 0.2)
print(len(train_set), "train +", len(test_set), "test")

from zlib import crc32


# def test_set_check(identifier, test_ratio):
#     return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2 ** 32


def split_train_test_by_id(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]


import hashlib


def test_set_check(identifier, test_ratio, hash=hashlib.md5):
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio


housing_with_id = housing.reset_index()  # adds an `index` column
train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "index")
print('===============================================================================================================')
print(train_set.head())

housing_with_id["id"] = housing["longitude"] * 1000 + housing["latitude"]
train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "id")
print('===============================================================================================================')
print(train_set.head())
print('===============================================================================================================')
print(test_set.head())

# sklearn train_test_split
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
print('===============================================================================================================')
print(train_set.head())

print('===============================================================================================================')
housing["median_income"].hist()
plt.show()

# Divide by 1.5 to limit the number of income categories
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)
# Label those above 5 as 5
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
print('===============================================================================================================')
print(housing["income_cat"].value_counts())
print('===============================================================================================================')
print(housing.head())

housing["income_cat"].hist()
plt.show()

from sklearn.model_selection import StratifiedShuffleSplit

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

print('===============================================================================================================')
print('All data income_cat distribution')
print(housing["income_cat"].value_counts() / len(housing))

print('===============================================================================================================')
print('Train data income_cat distribution')
print(strat_train_set["income_cat"].value_counts() / len(strat_train_set))

print('===============================================================================================================')
print('Test data income_cat distribution')
print(strat_test_set["income_cat"].value_counts() / len(strat_test_set))


def income_cat_proportions(data):
    return data["income_cat"].value_counts() / len(data)


train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

compare_props = pd.DataFrame({
    "Overall": income_cat_proportions(housing),
    "Stratified": income_cat_proportions(strat_test_set),
    "Random": income_cat_proportions(test_set),
}).sort_index()
compare_props["Rand. %error"] = 100 * compare_props["Random"] / compare_props["Overall"] - 100
compare_props["Strat. %error"] = 100 * compare_props["Stratified"] / compare_props["Overall"] - 100

print('===============================================================================================================')
print(compare_props)

for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

print('===============================================================================================================')
print(strat_train_set.head())

# Discover and visualize the data to gain insights

