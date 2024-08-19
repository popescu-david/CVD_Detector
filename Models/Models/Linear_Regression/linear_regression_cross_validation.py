import pandas as pd
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

data = pd.read_csv('Models/Datasets/logistic_processed_cardio_train.csv')

X = data.drop(columns=['Risc_Boală'])
y = data['Risc_Boală']

k = 10

kf = KFold(n_splits=k, shuffle=True, random_state=42)

mae_scores = []
mse_scores = []
rmse_scores = []

for train_index, test_index in kf.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mae_scores.append(mae)
    
    mse = mean_squared_error(y_test, y_pred)
    mse_scores.append(mse)
    
    rmse = np.sqrt(mse)
    rmse_scores.append(rmse)

average_mae = sum(mae_scores) / k
average_mse = sum(mse_scores) / k
average_rmse = sum(rmse_scores) / k

y_mean = np.mean(y)
nrmse = average_rmse / y_mean

print("Mean Absolute Error (MAE):", average_mae)
print("Mean Squared Error (MSE):", average_mse)
print("Root Mean Squared Error (RMSE):", average_rmse)
print("Normalized RMSE (NRMSE):", nrmse)
