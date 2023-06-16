import os
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter
from sklearn import model_selection
from sklearn.model_selection import KFold


candidate_col=[
    "Diastolic blood pressure",
    "Heart Rate",
    "Mean blood pressure",
    "Oxygen saturation",
    "Respiratory rate",
    "Systolic blood pressure",
]


def load_data(data="mixed"):
    fp = os.path.dirname(__file__)

    # # Sensor data
    # data = pd.read_csv(fp + "/PdM_telemetry.csv.gz")

    # # Error alarm logs
    # data = data.merge(
    #     pd.read_csv(fp + "/PdM_errors.csv.gz"), how="left", on=["datetime", "machineID"]
    # )

    # # Failure logs
    # data = data.merge(
    #     pd.read_csv(fp + "/PdM_failures.csv.gz"),
    #     how="left",
    #     on=["datetime", "machineID"],
    # )

    # # Formatting
    # data.datetime = pd.to_datetime(data.datetime)

    return data


def cleaning(df):

    # NaN values are encoded to -1
    df = df.sort_values("errorID")
    df.errorID = df.errorID.factorize()[0]
    df = df.sort_values("failure")
    df.failure = df.failure.factorize()[0]
    df = df.sort_values(["machineID", "datetime"])

    df.errorID = df.errorID.astype("int")
    df.failure = df.failure.astype("int")

    df.volt = df.volt.astype("float32")
    df.rotate = df.rotate.astype("float32")
    df.pressure = df.pressure.astype("float32")
    df.vibration = df.vibration.astype("float32")

    df.datetime = pd.to_datetime(df.datetime)
    return df