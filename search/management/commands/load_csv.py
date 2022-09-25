
from django.core.management import BaseCommand
from search.models import Patient, Pathology_TR, Procedure, RadiationFraction, Lab, ChemoPlan, ChemoCycle, RadiationSet
import pandas as pd
import numpy as np


duplicate_mrn_list = ['5777707', '70603027', '70845778', '90140756', '91068505', '91095083', '91648058', '91725790', '93901946', '93949662', '94538411']
primary_sites = ['C250', 'C251', 'C252', 'C253', 'C257', 'C258', 'C259']
class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        
        #Procedure.objects.all().delete()
        #Pathology_TR.objects.all().delete()
        #RadiationFraction.objects.all().delete()
        #RadiationSet.objects.all().delete()
        #Lab.objects.all().delete()
        #ChemoPlan.objects.all().delete()
        #ChemoCycle.objects.all().delete()
        #Patient.objects.all().delete()
        file_patient = 'search/data/2760.xlsx'
        file_lab = 'search/data/2760_lab.xlsx'
        #createPatient(file_patient)
        #createChemo(file_patient)
        #createRadiation(file_patient)
        #tumor_registry(file_patient)
        #createLab(file_lab)
        updatePatientDeath(file_patient)


def updatePatientDeath(file):
    df_diagnosis = pd.read_excel(file, sheet_name='diagnosis_TR')
    df_diagnosis = df_diagnosis.set_index('Medical Record Number')
    df_diagnosis.index = df_diagnosis.index.astype(str, copy = False)
    patients = Patient.objects.all()
    for patient in patients:
        
        if patient.date_of_death is None:
            patient.vital_status = 'Alive'
            mrn = patient.mrn
            if mrn in df_diagnosis.index:
                vital_status = df_diagnosis.at[mrn, 'Vital Status Value'] 
                if vital_status == '0 Dead (CoC)':
                    date_of_death = df_diagnosis.at[mrn, 'Date of Last Contact-Date'] 
                    patient.date_of_death = date_of_death
                    patient.vital_status = 'Dead'
        else:
            patient.vital_status = 'Dead'
        patient.save()
 
        
def createLab(file):
    df_lab = pd.read_excel(file, sheet_name='CA19-9')
    row_iter = df_lab.iterrows()
    objs = [

        Lab(
            name = 'CA19_9',
            value = row['ORD_VALUE'],
            date = row['RESULT_DATE'],
            patient = Patient.objects.get(mrn = row['pat_mrn_id'])
        )

        for index, row in row_iter

    ]
    Lab.objects.bulk_create(objs)

    df_lab = pd.read_excel(file, sheet_name='CEA')
    row_iter = df_lab.iterrows()
    objs = [

        Lab(
            name = 'CEA',
            value = row['ORD_VALUE'],
            date = row['RESULT_DATE'],
            patient = Patient.objects.get(mrn = row['pat_mrn_id'])
        )

        for index, row in row_iter

    ]
    Lab.objects.bulk_create(objs)
    df_lab = pd.read_excel(file, sheet_name='CBC')
    row_iter = df_lab.iterrows()
    objs = [

        Lab(
            name = 'CBC',
            value = row['ORD_VALUE'],
            date = row['RESULT_DATE'],
            patient = Patient.objects.get(mrn = row['pat_mrn_id'])
        )

        for index, row in row_iter

    ]
    Lab.objects.bulk_create(objs)
def createChemo(file):
    print("create chemo plan...")
    df_chemo = pd.read_excel(file, sheet_name='chemo')
    #filter out planted and Deleted chemo
    non_chemo_protocol = ['OP NORMAL SALINE INFUSION 250/500/1000ML W/WO MAGNESIUM, POTASSIUM, HEPARIN FLUSHES',\
        'TRANSFUSION - PRBC', 'TRANSFUSION - PRBC, PLT', 'OP SPLENECTOMY OR SICKLE CELL VACCINATIONS']
    df_chemo = df_chemo[df_chemo['CYCLE_STATUS_NAME'].isin(['Completed', 'Started'])]
    df_chemo = df_chemo[~df_chemo['PROTOCOL_NAME'].isin(non_chemo_protocol) ]
    df_chemo.dropna(subset=['PROTOCOL_NAME'], inplace=True)
    ser_chemo_cycle = df_chemo.groupby(['TREATMENT_PLAN_ID'], sort=False)['CYCLE_NUM'].max()

    df_chemo_plan = df_chemo[['MRN', 'TREATMENT_PLAN_ID', 'PLAN_START_DATE', 'PLAN_NAME']].drop_duplicates()
    df_chemo_plan['number_of_cycle'] = list(ser_chemo_cycle)
    row_iter = df_chemo_plan.iterrows()
    for index, row in row_iter:
        plan_id = row['TREATMENT_PLAN_ID']
        cycle = row['number_of_cycle']
        end_date = df_chemo.loc[(df_chemo['TREATMENT_PLAN_ID'] == plan_id) & (df_chemo['CYCLE_NUM'] == cycle)]['CYCLE_START_DATE'].iloc[0]
        df_chemo_plan.at[index, 'end_date'] = end_date

    row_iter = df_chemo_plan.iterrows()
    objs = [

        ChemoPlan(
            plan_id = row['TREATMENT_PLAN_ID'],
            plan = row['PLAN_NAME'],
            start_date = row['PLAN_START_DATE'],
            end_date = row['end_date'],
            patient = Patient.objects.get(mrn = row['MRN']),
            number_of_cycle = row['number_of_cycle']
        )

        for index, row in row_iter

    ]
    ChemoPlan.objects.bulk_create(objs)
    print("create chemo cycle...")
    row_iter = df_chemo.iterrows()
    objs = [

        ChemoCycle(
            protocol = row['PROTOCOL_NAME'],
            start_date = row['CYCLE_START_DATE'],
            cycle_number = row['CYCLE_NUM'],
            cycle_status = row['CYCLE_STATUS_NAME'],
            chemo_plan = ChemoPlan.objects.get(plan_id = row['TREATMENT_PLAN_ID']),
            patient = Patient.objects.get(mrn = row['MRN'])
        )

        for index, row in row_iter

    ]
    ChemoCycle.objects.bulk_create(objs)
    print("chemo created")


def createRadiation(file):
    print("Creating radiation sets records...")
    df_mosaiq = pd.read_excel(file, sheet_name='MOSAIQ')
    #filter out the treatment has 0 actual dose
    df_mosaiq = df_mosaiq[df_mosaiq['ACTUALTOTALDOSEINCGRAY'] > 0]

    ser_fraction = df_mosaiq.groupby(['SIT_SET_ID'], sort=False)['ACTUALFRACTIONS'].max()

    df_mosaiq_set = df_mosaiq[['MRN', 'SIT_SET_ID', 'START_DATE', 'SITE_NAME']].drop_duplicates()
    df_mosaiq_set['fractions'] = list(ser_fraction)
    row_iter = df_mosaiq_set.iterrows()
    for index, row in row_iter:
        set_id = row['SIT_SET_ID']
        fractions = row['fractions']
        end_date = df_mosaiq.loc[(df_mosaiq['SIT_SET_ID'] == set_id) & (df_mosaiq['ACTUALFRACTIONS'] == fractions)]['LAST_DATE'].iloc[0]
        df_mosaiq_set.at[index, 'end_date'] = end_date

        doses = df_mosaiq.loc[(df_mosaiq['SIT_SET_ID'] == set_id) & (df_mosaiq['ACTUALFRACTIONS'] == fractions)]['ACTUALTOTALDOSEINCGRAY'].iloc[0]
        df_mosaiq_set.at[index, 'doses'] = doses
    print(df_mosaiq_set.head())

    row_iter2 = df_mosaiq_set.iterrows()
    objs = [

        RadiationSet(
            set_id = row['SIT_SET_ID'],
            site_name = row['SITE_NAME'],
            start_date = row['START_DATE'],
            end_date = row['end_date'],
            patient = Patient.objects.get(mrn = row['MRN']),
            fractions = row['fractions'],
            doses = row['doses']
        )

        for index, row in row_iter2

    ]
    RadiationSet.objects.bulk_create(objs)
    print("create radiation fractions...")
    
    row_iter = df_mosaiq.iterrows()
    objs = [

        RadiationFraction(
            doses = row['ACTUALTOTALDOSEINCGRAY'],
            start_date = row['START_DATE'],
            end_date = row['LAST_DATE'],
            patient = Patient.objects.get(mrn = row['MRN']),
            fractions = row['ACTUALFRACTIONS'],
            site_name = row['SITE_NAME'],
            days_elapsed = row['ELAPSEDDAYS'],
            radiation_set = RadiationSet.objects.get(set_id = row['SIT_SET_ID']),
        )

        for index, row in row_iter

    ]
    RadiationFraction.objects.bulk_create(objs)
    print("Radiation fraction records are created")

def createPatient(file):
    print("Creating patients...")
    df_demographic = pd.read_excel(file, sheet_name='demographic')
    
    df_demographic = df_demographic[['MRN','GENDER', 'DEATH_DATE', 'latest_appt_date']]
    #df_demographic= df_demographic.replace({np.nan: None})

    df_diagnosis = pd.read_excel(file, sheet_name='diagnosis_TR')
    df_diagnosis['MRN'] = df_diagnosis['Medical Record Number']
    df_diagnosis = df_diagnosis[['MRN', 'Date of Diagnosis-Date', 'Age at Diagnosis', 'Vital Status Value']]
    df_demographic = df_demographic.merge(df_diagnosis, how = "left", left_on='MRN', right_on='MRN')
    df_demographic= df_demographic.replace({np.nan: None})
    
    row_iter1 = df_demographic.iterrows()
    objs1 = [

        Patient(
            mrn = row['MRN'],
            sex = row['GENDER'],
            age_at_diagnosis = row['Age at Diagnosis'],
            date_of_diagnosis = row['Date of Diagnosis-Date'],
            last_follow_up = row['latest_appt_date'],
            date_of_death = row['DEATH_DATE']
            
        )

        for index, row in row_iter1

    ]
    Patient.objects.bulk_create(objs1)
    print("Patients are created")
def tumor_registry(file):
    print('Created Tumor registry data...')
    df_tumor_registry = pd.read_excel(file, sheet_name='tumor-registry')
    #filter data only keep primary site in C250, C251, C252, C258
    df_tumor_registry = df_tumor_registry[df_tumor_registry['Primary Site'].isin(['C250', 'C251', 'C252', 'C253', 'C254', 'C255', 'C256', 'C257', 'C258', 'C259'])]
    df_tumor_registry['RX Date--Surgery'] = pd.to_datetime(df_tumor_registry['RX Date--Surgery'], format='%Y%m%d')
    df_tumor_registry['RX Date--Surgery'] = df_tumor_registry['RX Date--Surgery'] .replace({np.nan: None})
    for index, row in df_tumor_registry.iterrows():

        try:
            p = Patient.objects.get(mrn = row['Medical Record Number'])
        except:
            print("duplicated mrn:", row['Medical Record Number'])
            p = Patient.objects.filter(mrn = row['Medical Record Number'])[:1].get()
        
        #p = Patient.objects.get(mrn = row['Medical Record Number'])
        #print(row)
        pathology_TR = Pathology_TR(
            date_of_surgery = row['RX Date--Surgery'],
            node_category = row['Regional Nodes Positive Value'],
            lymph_vascular_invasion = row['Lymph-vascular Invasion Value'],
            tumor_grade = row['Grade Value'],
            surgical_margin = row['RX Summ--Surgical Margins Val'],
            location_of_tumor = row['Primary Site Value'],
            age_at_diagnosis = row['Age at Diagnosis'],
            date_of_diagnosis = row['Date of Diagnosis-Date'],
            patient = p


        )
        pathology_TR.save()
    print('Tumor registry data created')
def generate(file):
    print("loading data from file:", file)
    df_tumor_registry = pd.read_excel(file, sheet_name='tumor_registry')
    #filter data only keep primary site in C250, C251, C252, C258
    df_tumor_registry = df_tumor_registry[df_tumor_registry['Primary Site'].isin(['C250', 'C251', 'C252', 'C253', 'C254', 'C255', 'C256', 'C257', 'C258', 'C259'])]
    
    df_lab = pd.read_excel(file, sheet_name='CA 19-9')
    df_mosaiq = pd.read_excel(file, sheet_name='mosaiq')
    df_chemo = pd.read_excel(file, sheet_name='chemo')
    #filter out planted and Deleted chemo
    non_chemo_protocol = ['OP NORMAL SALINE INFUSION 250/500/1000ML W/WO MAGNESIUM, POTASSIUM, HEPARIN FLUSHES',\
        'TRANSFUSION - PRBC', 'TRANSFUSION - PRBC, PLT', 'OP SPLENECTOMY OR SICKLE CELL VACCINATIONS']
    df_chemo = df_chemo[df_chemo['CYCLE_STATUS_NAME'].isin(['Completed', 'Started'])]
    df_chemo = df_chemo[~df_chemo['PROTOCOL_NAME'].isin(non_chemo_protocol) ]
    df_chemo.dropna(subset=['PROTOCOL_NAME'], inplace=True)
    ser_chemo_cycle = df_chemo.groupby(['TREATMENT_PLAN_ID'], sort=False)['CYCLE_NUM'].max()

    df_chemo_plan = df_chemo[['MRN', 'TREATMENT_PLAN_ID', 'PLAN_START_DATE', 'PLAN_NAME']].drop_duplicates()
    df_chemo_plan['number_of_cycle'] = list(ser_chemo_cycle)
    row_iter = df_chemo_plan.iterrows()
    for index, row in row_iter:
        plan_id = row['TREATMENT_PLAN_ID']
        cycle = row['number_of_cycle']
        end_date = df_chemo.loc[(df_chemo['TREATMENT_PLAN_ID'] == plan_id) & (df_chemo['CYCLE_NUM'] == cycle)]['CYCLE_START_DATE'].iloc[0]
        df_chemo_plan.at[index, 'end_date'] = end_date

    
    df_smrtdta = pd.read_excel(file, sheet_name='smrtdta')
    columns_smrtdta = ['pat_mrn_id', 'ORDER_TIME', 'Procedure', 'Perineural Invasion', 'score']
    df_smrtdta = df_smrtdta[columns_smrtdta]

    df_demographic = pd.read_excel(file, sheet_name='demographic')
    
    df_demographic = df_demographic[['MRN','GENDER', 'DEATH_DATE', 'latest_appt_date']]
    #df_demographic = df_demographic.merge(df_tumor_registry, how='left', left_on='MRN', right_on='Medical Record Number')
    #columns_demo = ['MRN','GENDER', 'DEATH_DATE', 'latest_appt_date', 'Age at Diagnosis', 'Date of Diagnosis-Date']
    #df_demographic = df_demographic[columns_demo]
    df_demographic= df_demographic.replace({np.nan: None})
    
    row_iter1 = df_demographic.iterrows()
    objs1 = [

        Patient(
            mrn = row['MRN'],
            sex = row['GENDER'],
            #age_at_diagnosis = row['Age at Diagnosis'],
            #date_of_diagnosis = row['Date of Diagnosis-Date'],
            last_follow_up = row['latest_appt_date'],
            date_of_death = row['DEATH_DATE']
        )

        for index, row in row_iter1

    ]
    Patient.objects.bulk_create(objs1)
    
    
    df_tumor_registry['RX Date--Surgery'] = pd.to_datetime(df_tumor_registry['RX Date--Surgery'], format='%Y%m%d')
    df_tumor_registry['RX Date--Surgery'] = df_tumor_registry['RX Date--Surgery'] .replace({np.nan: None})
    df_smrtdta['ORDER_TIME'] = pd.to_datetime(df_smrtdta['ORDER_TIME']).dt.date
    df_smrtdta['ORDER_TIME'] = df_smrtdta['ORDER_TIME'].astype('datetime64[ns]')
    
    
    for index, row in df_tumor_registry.iterrows():

        try:
            p = Patient.objects.get(mrn = row['Medical Record Number'])
        except:
            print("duplicated mrn:", row['Medical Record Number'])
            p = Patient.objects.filter(mrn = row['Medical Record Number'])[:1].get()
        
        #p = Patient.objects.get(mrn = row['Medical Record Number'])
        #print(row)
        pathology_TR = Pathology_TR(
            date_of_surgery = row['RX Date--Surgery'],
            node_category = row['Regional Nodes Positive Value'],
            lymph_vascular_invasion = row['Lymph-vascular Invasion Value'],
            tumor_grade = row['Grade Value'],
            surgical_margin = row['RX Summ--Surgical Margins Val'],
            location_of_tumor = row['Primary Site Value'],
            age_at_diagnosis = row['Age at Diagnosis'],
            date_of_diagnosis = row['Date of Diagnosis-Date'],
            patient = p


        )
        pathology_TR.save()

    row_iter = df_mosaiq.iterrows()
    objs = [

        Radiation(
            doses = row['ACTUALTOTALDOSEINCGRAY'],
            start_date = row['START_DATE'],
            end_date = row['LAST_DATE'],
            patient = Patient.objects.get(mrn = row['MRN']),
            fractions = row['ACTUALFRACTIONS']
        )

        for index, row in row_iter

    ]
    Radiation.objects.bulk_create(objs)

    row_iter = df_lab.iterrows()
    objs = [

        Ca_19_9(
            value = row['ORD_VALUE'],
            date = row['RESULT_DATE'],
            patient = Patient.objects.get(mrn = row['pat_mrn_id'])
        )

        for index, row in row_iter

    ]
    Ca_19_9.objects.bulk_create(objs)
    
    
    
    row_iter = df_chemo_plan.iterrows()
    objs = [

        ChemoPlan(
            plan_id = row['TREATMENT_PLAN_ID'],
            plan = row['PLAN_NAME'],
            start_date = row['PLAN_START_DATE'],
            end_date = row['end_date'],
            patient = Patient.objects.get(mrn = row['MRN']),
            number_of_cycle = row['number_of_cycle']
        )

        for index, row in row_iter

    ]
    ChemoPlan.objects.bulk_create(objs)

    row_iter = df_chemo.iterrows()
    objs = [

        ChemoCycle(
            protocol = row['PROTOCOL_NAME'],
            start_date = row['CYCLE_START_DATE'],
            cycle_number = row['CYCLE_NUM'],
            cycle_status = row['CYCLE_STATUS_NAME'],
            chemo_plan = ChemoPlan.objects.get(plan_id = row['TREATMENT_PLAN_ID']),
            patient = Patient.objects.get(mrn = row['MRN'])
        )

        for index, row in row_iter

    ]
    ChemoCycle.objects.bulk_create(objs)

    df_smrtdta= df_smrtdta.replace({np.nan: None})

    row_iter = df_smrtdta.iterrows()
    objs = [

        Procedure(
            date = row['ORDER_TIME'],
            type_of_surgery = row['Procedure'],
            peri_neural_invasion = row['Perineural Invasion'],
            pathological_response = row['score'],
            patient = Patient.objects.get(mrn = row['pat_mrn_id'])
        )

        for index, row in row_iter

    ]
    Procedure.objects.bulk_create(objs)
    print('Number of patients uploaded:', df_demographic.shape[0])
        


        
        


        
        