import pandas as pd

cardio_train = pd.read_csv('Models/Datasets/cardio_train.csv')

# Remove the 'id' column
processed_cardio_train = cardio_train.drop('id', axis=1)

processed_cardio_train.to_csv('Models//Datasets/processed_cardio_train.csv', index=False)
