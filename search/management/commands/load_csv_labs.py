
import csv
from django.core.management import BaseCommand
from django.utils import timezone

from search.models import Lab, Patient

class Command(BaseCommand):
    help = "Loads products and product categories from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            labs = []
            for row in data:
                
                lab = Lab(
                    patient = Patient.objects.get(accession = row[0]),
                    name=row[1],
                    date=row[2],
                    value=row[3],
                )
                labs.append(lab)
                if len(labs) > 5000:
                    Lab.objects.bulk_create(labs)
                    labs = []
            if labs:
                Lab.objects.bulk_create(labs)
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )