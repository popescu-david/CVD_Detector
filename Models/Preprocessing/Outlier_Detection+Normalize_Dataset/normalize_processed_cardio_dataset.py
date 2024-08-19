import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

continuous_columns = ['Vârstă', 'Înălțime', 'Greutate', 'TAS', 'TAD']
categorical_columns = ['Colesterol', 'Glucoză']
binary_columns = ['Sex', 'Fumător', 'Băutor', 'Activitate']

def normalize_columns(df, scaler=None):
    if scaler is None:
        scaler = StandardScaler()
        df[continuous_columns] = scaler.fit_transform(df[continuous_columns])
        return df, scaler
    else:
        df[continuous_columns] = scaler.transform(df[continuous_columns])
        return df

csv_path = 'Models/Datasets/processed_cardio_train.csv'
output_path = 'Models/Datasets/normalized_cardio_train.csv'
scaler_path = 'Models/Models/scaler.pkl'

df = pd.read_csv(csv_path)

features = df.drop(columns=['Risc_Boală'])
target = df['Risc_Boală']

normalized_features, scaler = normalize_columns(features)
joblib.dump(scaler, scaler_path)

normalized_df = pd.concat([normalized_features, target], axis=1)

normalized_df.to_csv(output_path, index=False)