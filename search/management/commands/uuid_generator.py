import csv
from django.core.management import BaseCommand
from search.models import Patient
import uuid
from django.utils.crypto import get_random_string

import os

RANDOM_STRING_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class Command(BaseCommand):
    help = 'Generate uuid and accession for patients in the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        mrns = list(Patient.objects.values_list('mrn', flat=True))
        visited = []
        with open('uuids.csv', 'w', newline='') as output:
            writer = csv.writer(output, delimiter='\t')
            for mrn in mrns:
                if mrn not in visited:
                    myuuid = uuid.uuid4()
                    accession = get_random_string(8, RANDOM_STRING_CHARS)
                    writer.writerow([mrn, str(myuuid), accession])
                    visited.append(mrn)