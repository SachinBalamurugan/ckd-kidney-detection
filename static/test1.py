import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import warnings
warnings.filterwarnings(action='ignore')

data=pd.read_csv("dataset/kidney_disease.csv")
data.head(10)

data.columns

for i in data.drop("id",axis=1).columns:
    print('unique values in "{}":\n'.format(i),data[i].unique())

#data.info()
data.describe()
