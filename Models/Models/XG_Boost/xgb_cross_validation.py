import pandas as pd
import xgboost as xgb
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

np.random.seed(42)
data = pd.read_csv('Models/Datasets/xgb_processed_cardio_train.csv')

X = data.drop(columns=['Risc_Boală'])
y = data['Risc_Boală']

k = 10

kf = KFold(n_splits=k, shuffle=True, random_state=42)

mae_scores = []
mse_scores = []
rmse_scores = []

dtrain = xgb.DMatrix(X, label=y)

params = {
    'objective': 'reg:squarederror',
    'seed': 42
}

for train_index, test_index in kf.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    dtrain_fold = xgb.DMatrix(X_train, label=y_train)
    dtest_fold = xgb.DMatrix(X_test, label=y_test)
    
    model = xgb.train(params, dtrain_fold)
    
    y_pred = model.predict(dtest_fold)
    
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
