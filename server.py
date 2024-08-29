from os import getenv, path
from flask import Flask, request, send_file
from dotenv import load_dotenv
import requests
import csv
from constants import ACCESS_KEYS_PATH
from plot_activities import plot_activities
from save_activities import save_activities

load_dotenv()

app = Flask(__name__)

client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")


@app.route("/get-auth-url")
def get_auth_url():
    redirect_uri = getenv("REDIRECT_URI")
    scope = "read_all,activity:read_all"
    url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}/exchange_token&approval_prompt=force&scope={scope}"
    return f"<a target=_blank href={url}>auth url</a>"


@app.route("/exchange_token")
def authenticate():
    code = request.args.get("code")
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    response_data = response.json()
    access_token = response_data["access_token"]
    user_id = response_data["athlete"]["id"]
    path_to_csv_file = ACCESS_KEYS_PATH
    file_exists = path.isfile(path_to_csv_file)

    if not file_exists:
        with open(path_to_csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "access_token"])

    rows = []
    user_exists = False
    with open(path_to_csv_file, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(user_id):
                row[1] = access_token
                user_exists = True
            rows.append(row)

    if not user_exists:
        rows.append([user_id, access_token])

    with open(path_to_csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return f"user_id: {user_id}"


@app.route("/save-activities")
def save_user_activities():
    user_id = request.args.get("user_id")
    try:
        save_activities(user_id)
        return "Activities saved!"
    except Exception as e:
        print("error:", e)
        return "Error saving activities"


@app.route("/plot-activities")
def plot_user_activities():
    user_id = request.args.get("user_id")
    activity_type = request.args.get("activity_type")
    try:
        img = plot_activities(user_id, activity_type)
        return send_file(
            img,
            mimetype="image/png",
            as_attachment=False,
            download_name=f"{user_id}_activities.png",
        )
    except Exception as e:
        print("error:", e)
        return "Error plotting activities"


if __name__ == "__main__":
    app.run(port=8080, debug=True)
