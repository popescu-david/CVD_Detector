import csv
from datetime import datetime
from Detector.models import Patients

def import_data_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            patient = Patients.objects.create(
                ssn=row['ssn'],
                firstname=row['firstname'],
                lastname=row['lastname'],
                email=row['email'],
                age=int(row['age']),
                gender=int(row['gender']),
                height=float(row['height']),
                weight=float(row['weight']),
                ap_hi=int(row['ap_hi']),
                ap_lo=int(row['ap_lo']),
                cholesterol=int(row['cholesterol']),
                gluc=int(row['gluc']),
                smoke=int(row['smoke']),
                alco=int(row['alco']),
                active=int(row['active']),
                cardio=int(row['cardio']),
                entry_creation_date=datetime.strptime(row['entry_creation_date'], '%Y%m%d').date()
            )
            patient.save()

csv_file_path = 'Models/Datasets/enhanced_cardio_train.csv'
import_data_from_csv(csv_file_path)