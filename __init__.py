import os
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter
from sklearn import model_selection, preprocessing
from sklearn.model_selection import KFold


columns=[
    "Diastolic blood pressure",
    "Heart Rate",
    "Mean blood pressure",
    "Oxygen saturation",
    "Respiratory rate",
    "Systolic blood pressure",
]


def load_data(data="Mixed"):
    fp = os.path.dirname(__file__)
    sequene_names = os.listdir(f"{fp}/preprocessed/{data}")
    sequene_names.remove("class.csv")
    sequene_names = sorted(sequene_names)

    data_list = []
    class_list = []

   # Encode categorical class label
    oe = preprocessing.OrdinalEncoder()
    class_df = pd.read_csv(f"{fp}/preprocessed/{data}/class.csv")
    class_df["Class_encoded"] = oe.fit_transform(class_df["Class"])


    for patient_id, name in enumerate(sequene_names):
        class_id = class_df[class_df["stay"] == name]["Class_encoded"]
        temp_df = pd.read_csv(f"{fp}/preprocessed/{data}/{name}")
        temp_df["patient_id"] = patient_id
        temp_df["Class"] = class_id
        data_list.append(temp_df)

    data_df = pd.concat(data_list,axis=0)

    return data


def cleaning(df):
    df = df[["Hours","patient_id","Class"] + columns]

    return df

def add_rul(concatenated_df):
    label_name = "Time_to_Event" 
    df_list = []
    for id_, df in concatenated_df.groupby("patient_id"):
        df = df.sort_values("Hours")
        time_array = np.arange(len(df))[::-1]
        df[label_name] = time_array
        df_list.append(df)
        
    return df_list


def load_clean_data_rul_k_folds(
    data,
    split_ind,
    k=5,
    random_state=0,
):
    df_list = add_rul((cleaning(load_data(data=data))))

    data_index = range(len(df_list))

    kf = KFold(
        n_splits=k,
        random_state=random_state,
        shuffle=True,
    )

    train_idx, test_idx = list(kf.split(data_index))[split_ind]

    train_df_list = [df_list[i] for i in train_idx]
    test_df_list = [df_list[i] for i in test_idx]

    return train_df_list, test_df_list