import requests
import pandas as pd
import csv
import os
from dotenv import load_dotenv

from src.constants import ACCESS_KEYS_PATH

load_dotenv()


def save_activities(user_id):

    def get_access_token_from_csv_file(user_id):
        access_token = None
        try:
            with open(ACCESS_KEYS_PATH, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["user_id"] == str(user_id):
                        access_token = row["access_token"]
                        break
            return access_token
        except Exception:
            return None

    try:
        access_token = get_access_token_from_csv_file(user_id)
    except Exception as e:
        raise Exception(f"Error getting access token: {e}")
    page = 1
    page_size = 200

    headers = {"Authorization": f"Bearer {access_token}"}

    api_response = None
    csv_filename = os.path.join(os.getcwd(), f"data/{user_id}_activities.csv")

    with open(csv_filename, mode="w", newline="") as file:
        file.write("")  # Create an empty file

    # Track columns to maintain consistency
    columns = None

    while True:
        params = {"page": page, "per_page": page_size}
        try:
            response = requests.get(
                "https://www.strava.com/api/v3/athlete/activities",
                headers=headers,
                params=params,
            )

            response.raise_for_status()

            api_response = response.json()

            if not api_response:
                break

            # Convert API response to DataFrame
            df = pd.DataFrame(api_response)

            # Update columns if they are not set
            if columns is None:
                columns = df.columns

            # Ensure the DataFrame has the same columns
            df = df[columns]

            # Append DataFrame to CSV
            df.to_csv(
                csv_filename,
                mode="a",
                header=not os.path.getsize(csv_filename) > 0,
                index=False,
            )

            page += 1

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    print(f"Activities saved to {csv_filename}")
