import csv
from os import getenv, path
from flask import Blueprint, request, send_file
import requests
from dotenv import load_dotenv
from constants import ACCESS_KEYS_FILE_HEADERS, ACCESS_KEYS_PATH

load_dotenv()


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")


@auth_bp.route("/get-auth-url")
def get_auth_url():
    redirect_uri = getenv("REDIRECT_URI")
    scope = "read_all,activity:read_all"
    url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}/auth/exchange_token&approval_prompt=force&scope={scope}"
    return f"<a target=_blank href={url}>auth url</a>"


@auth_bp.route("/exchange_token")
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
            writer.writerow(ACCESS_KEYS_FILE_HEADERS)

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
