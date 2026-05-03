import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import confusion_matrix,accuracy_score

import os
df = pd.read_csv('dataset/kidney_disease.csv')

### Run this to Profile data

import pandas_profiling as pp

profile = pp.ProfileReport(df, title="Chronic Kidney Disease Profile", html={"style": {"full_width": True}}, sort=None)
profile


'''profile = df.profile_report(
    sort="ascending",
    vars={
        "num": {"low_categorical_threshold": 0},
        "cat": {
            "length": True,
            "characters": False,
            "words": False,
            "n_obs": 5,
        },
    },
)

profile.config.variables.descriptions = {
    "files": "Files in the filesystem",
    "datec": "Creation date",
    "datem": "Modification date",
}

profile.to_file("report.html")'''
