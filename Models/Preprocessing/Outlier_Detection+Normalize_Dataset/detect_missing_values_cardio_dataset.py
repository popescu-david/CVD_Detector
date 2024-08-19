import pandas as pd
csv_filename = 'Models/Datasets/cardio_train.csv'
df = pd.read_csv(csv_filename)
na_counts = df.isna().sum()
print(na_counts)