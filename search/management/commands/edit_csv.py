import csv
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Edit csv file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        output = open('output.csv', 'w', newline='')
        data = []

        with open(path, 'rt') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                rowData = [row[0], row[7], row[1], row[2], row[3], row[4], row[5], row[6], row[8], row[9]]
                data.append(rowData)
        with output:
            writer = csv.writer(output, delimiter='\t')
            writer.writerows(data)