import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

data = pd.read_csv("Models/Datasets/rf_processed_cardio_train.csv")

X = data.drop(columns=['Risc_Boală'])
y = data['Risc_Boală']

model = RandomForestRegressor(n_estimators=250, random_state=42)
model.fit(X, y)

joblib.dump(model, 'Models/Models/Random_Forest/rf_model.pkl')
