
from datetime import datetime
from django.core.management import BaseCommand
from numpy import datetime64
from search.models import Patient, Pathology, Procedure, Radiation, Ca_19_9, ChemoPlan, ChemoCycle
import pandas as pd
import numpy as np
import csv

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        file = 'search/data/data_peter.xlsx'
        df = pd.read_excel(file, sheet_name='neoadjuvant SBRT')
        df_radiation = pd.read_excel(file, sheet_name='Neoadjuvant SBRT radiation')
        df_radiation = df_radiation.set_index(['MRN'])
        output = 'search/data/check.csv'
        csv_file = open(output, "w",newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['source', 'mrn', 'sex', 'date_of_diagnosis', 'age_at_diagnosis', 'last_follow_up', 'date_of_death', 'date_of_surgery', \
                'lymph_vascular_invasion', 'tumor_grade', 'surgical_margin', 'location_of_tumor', 'type_of_surgery', \
                'pathological_response', 'radiation_doses', 'radiation_fractions', 'radiation_start_date', 'radiation_end_date'])

        row_iter = df.iterrows()
        for index, row in row_iter:
            mrn = int(row['Medical Record Number'])
            sex = 'MALE'
            if row['Sex'] == 2:
                sex = 'FEMALE'
            date_of_diagnosis = row['Date of Diagnosis-Date'].date()
            age_at_diagnosis = row['Age at Diagnosis (years)']
            date_of_death = row['Vital Status']
            last_follow_up = row['Date of Last Contact-Date'].date()
            date_of_surgery = row['RX Date--Most Defin Surg-Date'].date()
            lymph_vascular_invasion = row['Lymph-vascular Invasion']
            tumor_grade = row['Grade']
            surgical_margin = row['Surgical margins (1=+ve)']
            location_of_tumor = 'body/tail'
            if row['tumor site'] == 1:
                location_of_tumor = 'head/neck/uncinate process'
            elif row['tumor site'] == 9:
                location_of_tumor = 'missing data'
            type_of_surgery = 'distal pancreatectomy'
            if row['Surgery procedure'] == 1:
                type_of_surgery = 'all others'
            elif row['Surgery procedure'] == 9:
                location_of_tumor = 'missing data'        
            pathological_response = row['Pathological response score']
            #get radiation data
            radiation = df_radiation.loc[int(mrn)]
            doses = radiation['Dose[cGy](Actual)']
            fractions = radiation['Fractions(Actual)']
            start_date = radiation['StartDate'].date()
            end_date = radiation['LastDate'].date()

            writer.writerow(['Peter', mrn, sex, date_of_diagnosis, age_at_diagnosis, last_follow_up, date_of_death, \
                date_of_surgery, lymph_vascular_invasion, tumor_grade, surgical_margin, location_of_tumor, \
                type_of_surgery, pathological_response, doses, fractions, start_date, end_date])
            p = Patient.objects.get(mrn=mrn)
            print(type( p.date_of_death))
            new_row = ['database', p.mrn, p.sex, p.date_of_diagnosis, p.age_at_diagnosis, p.last_follow_up, p.date_of_death]
            try:
                path = Pathology.objects.filter(patient__mrn = mrn)[:1].get()
                new_row = new_row + [path.date_of_surgery, path.lymph_vascular_invasion[0], path.tumor_grade[0], path.surgical_margin[0], path.location_of_tumor]
            except Pathology.DoesNotExist:
                path = None
                new_row = new_row + ['NA', 'NA', 'NA', 'NA', 'NA']
            try:
                procedure = Procedure.objects.filter(patient__mrn = mrn)[:1].get()
                new_row = new_row + [procedure.type_of_surgery, procedure.pathological_response]
            except Procedure.DoesNotExist:
                new_row = new_row + ['NA', 'NA']

            try:
                r = Radiation.objects.filter(patient__mrn = mrn)[:1].get()
                new_row = new_row + [r.doses, r.fractions, r.start_date, r.end_date]
            except Radiation.DoesNotExist:
                new_row = new_row + ['NA', 'NA', 'NA', 'NA']

            writer.writerow(new_row)
        csv_file.close()




     