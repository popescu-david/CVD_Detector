import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data = pd.read_csv('Models/Datasets/enhanced_cardio_train.csv')

X = data.drop(['Risc_Boală','NSS','Prenume','Nume','Email','Dată_Adăugare'], axis=1)
y = data['Risc_Boală']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train, y_train)

full_probabilities = logistic_model.predict_proba(X)[:, 1]

data['Risc_Boală'] = full_probabilities

data.to_csv('Models/Datasets/logistic_enhanced_cardio_train.csv', index=False)

print(full_probabilities)
