import matplotlib.pyplot as plt
import numpy as np

from plotting.common import (
    convert_to_png,
    filter_by_activity_type,
    get_activities_data_frame_from_csv,
    set_distance_units,
)

plt.switch_backend("Agg")


def get_histogram(user_id, activity_type, distance_unit):
    activities_df = filter_by_activity_type(
        get_activities_data_frame_from_csv(user_id), activity_type
    )
    activities_df = set_distance_units(activities_df, distance_unit)

    max_distance = activities_df["distance"].max()
    bins = int(max_distance * 2)
    max_frequency = np.histogram(activities_df["distance"], bins)[0].max()

    plt.figure(figsize=(20, 6))

    plt.hist(
        activities_df["distance"],
        bins,
        color="pink",
        edgecolor="black",
        histtype="barstacked",
    )

    plt.title(f"Distribution of {activity_type} Distances")
    plt.xlabel("Distance (km)")
    plt.ylabel("Frequency")

    set_ticks(max_distance, max_frequency)

    return convert_to_png()


def set_ticks(max_distance, max_frequency):
    x_ticks = np.arange(1, max_distance, 1)
    y_ticks = np.arange(0, max_frequency, 5)

    if max_distance % 1 != 0:
        x_ticks = np.append(x_ticks, int(max_distance))
    if max_frequency % 5 != 0:
        y_ticks = np.append(y_ticks, max_frequency)

    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    ax = plt.gca()
    x_labels, y_labels = ax.get_xticklabels(), ax.get_yticklabels()

    x_labels[-1].set_color("green")
    y_labels[-1].set_color("green")
