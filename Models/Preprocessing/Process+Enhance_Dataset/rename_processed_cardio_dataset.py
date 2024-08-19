import pandas as pd

input_file = 'Models/Datasets/processed_cardio_train.csv'
output_file = 'Models/Datasets/processed_cardio_train.csv'

data = pd.read_csv(input_file)

column_mapping = {
    'age': 'Vârstă',
    'gender': 'Sex',
    'height': 'Înălțime',
    'weight': 'Greutate',
    'ap_hi': 'TAS',
    'ap_lo': 'TAD',
    'cholesterol': 'Colesterol',
    'gluc': 'Glucoză',
    'smoke': 'Fumător',
    'alco': 'Băutor',
    'active': 'Activitate',
    'cardio': 'Risc_Boală'
}

data.rename(columns=column_mapping, inplace=True)

data.to_csv(output_file, index=False)
