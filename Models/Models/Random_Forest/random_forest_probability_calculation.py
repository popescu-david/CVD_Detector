import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('Models/Datasets/normalized_cardio_train.csv')

X = data.drop('Risc_Boală', axis=1)
y = data['Risc_Boală']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

rf_classifier = RandomForestClassifier(n_estimators=250, random_state=42)
rf_classifier.fit(X_train, y_train)

full_probabilities = rf_classifier.predict_proba(X)[:, 1]

data['Risc_Boală'] = full_probabilities

data.to_csv('Models/Datasets/rf_processed_cardio_train.csv', index=False)

print(full_probabilities)
