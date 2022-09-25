from django.core.management import BaseCommand
from django.db.models import F
from search.models import Patient, Pathology_TR, RadiationSet, RadiationFraction, ChemoPlan, ChemoCycle
from datetime import timedelta

NUMBER_OF_DAYS = None
class Command(BaseCommand):
    help = 'update uuid and accession for patients in the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        #Patient.objects.all().update(date_of_death=F('date_of_death') - timedelta(days=NUMBER_OF_DAYS) )
        Patient.objects.all().update(date_of_diagnosis=F('date_of_diagnosis') - timedelta(days=NUMBER_OF_DAYS))
        Patient.objects.all().update(last_follow_up=F('last_follow_up') - timedelta(days=NUMBER_OF_DAYS))
        Pathology_TR.objects.all().update(date_of_surgery=F('date_of_surgery') - timedelta(days=NUMBER_OF_DAYS))
        Pathology_TR.objects.all().update(date_of_diagnosis=F('date_of_diagnosis') - timedelta(days=NUMBER_OF_DAYS))
        RadiationSet.objects.all().update(start_date=F('start_date') - timedelta(days=NUMBER_OF_DAYS))
        RadiationSet.objects.all().update(end_date=F('end_date') - timedelta(days=NUMBER_OF_DAYS))
        RadiationFraction.objects.all().update(start_date=F('start_date') - timedelta(days=NUMBER_OF_DAYS))
        RadiationFraction.objects.all().update(end_date=F('end_date') - timedelta(days=NUMBER_OF_DAYS))
        ChemoPlan.objects.all().update(start_date=F('start_date') - timedelta(days=NUMBER_OF_DAYS))
        ChemoPlan.objects.all().update(end_date=F('end_date') - timedelta(days=NUMBER_OF_DAYS))
        ChemoCycle.objects.all().update(start_date=F('start_date') - timedelta(days=NUMBER_OF_DAYS))


       
       
        
        