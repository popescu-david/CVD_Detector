import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import numpy as np

np.random.seed(42)

data = pd.read_csv('Models/Datasets/enhanced_cardio_train.csv')

X = data.drop(['Risc_Boală','NSS','Prenume','Nume','Email','Dată_Adăugare'], axis=1)
y = data['Risc_Boală']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')

model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)

full_probabilities = model.predict_proba(X)[:, 1]

data['Risc_Boală'] = full_probabilities

print(full_probabilities)

data.to_csv('Models/Datasets/xgb_enhanced_cardio_train.csv', index=False)