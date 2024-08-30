from io import BytesIO
import os
from matplotlib import pyplot as plt
import pandas as pd


def get_activities_data_frame_from_csv(user_id) -> pd.DataFrame:
    data_file_path = os.path.join(os.getcwd(), f"data/{user_id}_activities.csv")
    data = pd.read_csv(data_file_path)
    return data


def filter_by_activity_type(data: pd.DataFrame, activity_type) -> pd.DataFrame:
    activities_df = data.loc[data["type"] == activity_type]

    return activities_df


def set_distance_units(data: pd.DataFrame, distance_unit):
    data.loc[:, "distance"] = data["distance"] / 1000

    if distance_unit == "mi":
        data.loc[:, "distance"] = data["distance"] * 0.621371

    return data


def convert_to_png():
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return buf
