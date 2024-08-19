import pandas as pd
import requests

url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/most-common-name/surnames.csv"

try:
    response = requests.get(url)
    response.raise_for_status()

    df = pd.read_csv(url)

    csv_filename = 'Models/Datasets/last_names.csv'

    df.to_csv(csv_filename, index=False)

    print(f"Data copied to '{csv_filename}' successfully.")

except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error occurred: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Other Error: {err}")
except Exception as e:
    print(f"An error occurred: {e}")