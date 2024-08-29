from flask import Blueprint, request

from save_activities import save_activities


activities_bp = Blueprint("activities", __name__, url_prefix="/activities")


@activities_bp.route("/save-activities")
def save_user_activities():
    user_id = request.args.get("user_id")
    try:
        save_activities(user_id)
        return "Activities saved!"
    except Exception as e:
        print("error:", e)
        return "Error saving activities"
