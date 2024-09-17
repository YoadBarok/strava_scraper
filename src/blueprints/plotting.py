from flask import Blueprint, request, send_file

from src.plotting.histogram import get_histogram

plotting_bp = Blueprint("plotting", __name__, url_prefix="/plotting")


@plotting_bp.route("/histogram")
def plot_histogram():
    user_id = request.args.get("user_id")
    activity_type = request.args.get("activity_type") or "Run"
    distance_unit = request.args.get("distance_unit") or "km"
    try:
        histogram = get_histogram(user_id, activity_type, distance_unit)
        return send_file(
            histogram,
            mimetype="image/png",
            as_attachment=False,
            download_name=f"{user_id}_activities.png",
        )
    except Exception as e:
        print("ERROR ERROR")
        print("error:", e)
        return "Error plotting activities"
