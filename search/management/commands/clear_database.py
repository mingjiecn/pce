import csv
from django.core.management import BaseCommand
from search.models import Patient, Pathology_TR, Procedure, RadiationFraction, Lab, ChemoPlan, ChemoCycle, RadiationSet

import os

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--model', type=str)

    def handle(self, *args, **kwargs):

        if kwargs['model'] == 'Patient':
            Patient.objects.all().delete()
            print("Patient data is deleted")
        elif kwargs['model'] == 'Pathology_TR':
            Pathology_TR.objects.all().delete()
            print("Pathology_TR data is deleted")
        elif kwargs['model'] == 'Procedure':
            Procedure.objects.all().delete()
            print("Procedure data is deleted")
        elif kwargs['model'] == 'RadiationFraction':
            RadiationFraction.objects.all().delete()
            print("RadiationFraction data is deleted")
        elif kwargs['model'] == 'Lab':
            Lab.objects.all().delete()
            print("Lab data is deleted")
        elif kwargs['model'] == 'ChemoPlan':
            ChemoPlan.objects.all().delete()
            print("ChemoPlan data is deleted")
        elif kwargs['model'] == 'ChemoCycle':
            ChemoCycle.objects.all().delete()
            print("ChemoCycle data is deleted")
        elif kwargs['model'] == 'RadiationSet':
            RadiationSet.objects.all().delete()
            print("RadiationSet data is deleted")


                
                