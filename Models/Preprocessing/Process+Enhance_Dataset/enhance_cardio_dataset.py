import pandas as pd
import random
from datetime import datetime, timedelta

def generate_random_ssn():
    ssn = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return ssn

def generate_random_date(start_date, end_date):
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def enhance_cardio_train(input_csv_file, female_first_names_csv_file, male_first_names_csv_file, last_names_csv_file, output_csv_file):

    df_cardio = pd.read_csv(input_csv_file)

    df_female_first_names = pd.read_csv(female_first_names_csv_file)['name'].tolist()

    df_male_first_names = pd.read_csv(male_first_names_csv_file)['name'].tolist()

    df_last_names = pd.read_csv(last_names_csv_file)['name'].tolist()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=3652)

    for index, row in df_cardio.iterrows():
        gender = row['gender']

        if gender == 1:
            firstname = random.choice(df_female_first_names)
        elif gender == 2:
            firstname = random.choice(df_male_first_names)
        else:
            firstname = 'Unknown'

        lastname = random.choice(df_last_names)

        firstname_str = str(firstname) if isinstance(firstname, str) else 'Unknown'
        lastname_str = str(lastname) if isinstance(lastname, str) else 'Unknown'
        email = f"{firstname_str.lower()}.{lastname_str.lower()}@email.com"

        ssn = generate_random_ssn()

        entry_creation_date = generate_random_date(start_date, end_date)

        df_cardio.at[index, 'firstname'] = firstname_str
        df_cardio.at[index, 'lastname'] = lastname_str
        df_cardio.at[index, 'email'] = email
        df_cardio.at[index, 'ssn'] = ssn
        df_cardio.at[index, 'entry_creation_date'] = entry_creation_date.strftime('%Y%m%d')

    ordered_columns = ['ssn', 'firstname', 'lastname', 'email'] + [col for col in df_cardio.columns if col not in ['id', 'firstname', 'lastname', 'email', 'ssn', 'entry_creation_date']] + ['entry_creation_date']
    df_cardio = df_cardio[ordered_columns]

    df_cardio.to_csv(output_csv_file, index=False)

input_csv_file = 'Models/Datasets/cardio_train.csv'
female_first_names_csv_file = 'Models/Datasets/female_first_names.csv'
male_first_names_csv_file = 'Models/Datasets/male_first_names.csv'
last_names_csv_file = 'Models/Datasets/last_names.csv'
output_csv_file = 'Models/Datasets/enhanced_cardio_train.csv'

enhance_cardio_train(input_csv_file, female_first_names_csv_file, male_first_names_csv_file, last_names_csv_file, output_csv_file)
