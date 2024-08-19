import pandas as pd
import xgboost as xgb
import joblib
import numpy as np

np.random.seed(42)
data = pd.read_csv("Models/Datasets/xgb_processed_cardio_train.csv")

X = data.drop(columns=['Risc_Boală'])
y = data['Risc_Boală']

model = xgb.XGBRegressor()
model.fit(X, y)

joblib.dump(model, 'Models/Models/XG_Boost/xgb_model.pkl')