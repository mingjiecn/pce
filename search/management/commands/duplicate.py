
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
        for mrn in Patient.objects.values_list('mrn', flat=True).distinct():
            size = len(Patient.objects.filter(mrn=mrn))
            if size > 1: 
                print(mrn)
