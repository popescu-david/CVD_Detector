import pandas as pd

input_csv_file = 'Models/Datasets/first_names.csv'

df_first_names = pd.read_csv(input_csv_file)

df_female_names = df_first_names[df_first_names['gender'] == 1]
df_male_names = df_first_names[df_first_names['gender'] == 2]

df_female_names.drop(columns=['gender'], inplace=True)
df_male_names.drop(columns=['gender'], inplace=True)

output_female_csv_file = 'Models/Datasets/female_first_names.csv'
output_male_csv_file = 'Models/Datasets/male_first_names.csv'

df_female_names.to_csv(output_female_csv_file, index=False)

df_male_names.to_csv(output_male_csv_file, index=False)