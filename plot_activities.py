from io import BytesIO
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend("Agg")


def plot_activities(user_id, activity_type):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    activities_file_path = os.path.join(current_dir, f"data/{user_id}_activities.csv")
    df = pd.read_csv(activities_file_path, on_bad_lines="skip")

    df["distance"] = pd.to_numeric(df["distance"], errors="coerce") / 1000

    run_activities_df = df[df["type"] == activity_type]

    plt.figure(figsize=(20, 6))

    plt.hist(
        run_activities_df["distance"],
        bins=100,
        color="blue",
        edgecolor="black",
    )

    plt.title("Distribution of Run Distances")
    plt.xlabel("Distance (km)")
    plt.ylabel("Frequency")
    print(run_activities_df["distance"].max())

    plt.xticks(np.arange(0, run_activities_df["distance"].max() + 1, 1))
    plt.yticks(np.arange(0, plt.gca().get_ylim()[1] + 5, 5))

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return buf
