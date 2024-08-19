import pandas as pd
from sklearn.ensemble import IsolationForest

data = pd.read_csv('Models/Datasets/processed_cardio_train.csv')

iso_forest = IsolationForest(contamination=0.001, random_state=42)
iso_forest.fit(data)

outliers = iso_forest.predict(data)

inliers_mask = outliers == 1

inliers_data = data[inliers_mask]

print("Number of inliers:", len(inliers_data))
print(inliers_data.head())

inliers_data.to_csv('Models/Datasets/processed_cardio_train.csv', index=False)