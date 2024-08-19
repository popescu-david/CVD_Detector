from ucimlrepo import fetch_ucirepo
import pandas as pd

try:
    gender_by_name = fetch_ucirepo(id=591)

    X = gender_by_name.data.features
    feature_names = gender_by_name.data.feature_names

    df = pd.DataFrame(X, columns=feature_names)

    csv_filename = 'Models/Datasets/first_names.csv'

    df.to_csv(csv_filename, index=False)

    print(f"Dataset features saved to '{csv_filename}' successfully.")

except Exception as e:
    print(f"An error occurred: {e}")