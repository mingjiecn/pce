
from datetime import datetime
from django.core.management import BaseCommand
from numpy import datetime64
from search.models import Patient, Pathology_TR, Procedure, Radiation, Ca_19_9, ChemoPlan, ChemoCycle
import pandas as pd
import numpy as np
import csv

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        patient_set = Patient.objects.all()
        for patient in patient_set.iterator():
            mrn = patient.mrn
            try:
                #right now use data from tumor registry, this may change.
                #One patient may have more then one TR entry
                path = Pathology_TR.objects.filter(patient__mrn = mrn).order_by('date_of_diagnosis')[:1].get()

            except Pathology_TR.DoesNotExist:
                path = None

            if path is not None:
                patient.date_of_diagnosis = path.date_of_diagnosis
                patient.age_at_diagnosis = path.age_at_diagnosis
                surgery_date = path.date_of_surgery
                #decide the categary
                #find the radiation date
                try:
                    radiation = Radiation.objects.filter(patient__mrn = mrn).order_by('start_date')[:1].get()

                except Radiation.DoesNotExist:
                    radiation = None
                if radiation is not None:
                    radiation_date = radiation.start_date
                    fractions = radiation.fractions
                    if fractions <= 5:
                        is_SABR = True
                        if surgery_date is not None and radiation_date < surgery_date:
                            patient.category = 'NA SABR'
                    else:
                        is_SABR = False
                else:
                    radiation_date = None
                
                #find the Chemo date
                try:
                    chemo = ChemoPlan.objects.filter(patient__mrn = mrn).order_by('start_date')[:1].get()

                except ChemoPlan.DoesNotExist:
                    chemo = None
                if chemo is not None:
                    chemo_date = chemo.start_date
                else:
                    chemo_date = None

                patient.save()


                    
                
                
            



