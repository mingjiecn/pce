from django.core.management import BaseCommand
from django.db.models.functions import Cast
from search.models import Patient, Pathology_TR
from django.db import transaction

class Command(BaseCommand):
    help = 'update uuid and accession for patients in the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            patients = Patient.objects.all()
            for patient in patients:
                age = patient.age_at_diagnosis
                uuid = patient.uuid
                if age and age > 89:
                    Patient.objects.filter(uuid=uuid).update(age_at_diagnosis=90)

        with transaction.atomic():
            paths = Pathology_TR.objects.all()
            for path in paths:
                age = path.age_at_diagnosis
                if age > 89:
                    patient_id = path.patient_id
                    Pathology_TR.objects.filter(patient_id=patient_id).update(age_at_diagnosis=90)
 

                

