import csv
from django.core.management import BaseCommand
from search.models import Patient
from django.db import transaction

class Command(BaseCommand):
    help = 'update uuid and accession for patients in the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        with open('uuids.csv', 'rt') as f:
            reader = csv.reader(f, delimiter='\t')
            with transaction.atomic():
                for row in reader:
                    mrn = row[0]
                    uuid = row[1]
                    accession = row[2]
                    Patient.objects.filter(mrn=mrn).update(uuid=uuid, accession=accession)