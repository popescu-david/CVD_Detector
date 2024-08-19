import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = pd.read_csv("Models/Datasets/logistic_processed_cardio_train.csv")

X = data.drop(columns=['Risc_Boală'])
y = data['Risc_Boală']

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, 'Models/Models/Linear_Regression/linear_model.pkl')
