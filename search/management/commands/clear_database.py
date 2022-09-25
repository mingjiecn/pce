import csv
from django.core.management import BaseCommand
from search.models import Inguinal_male_protein_1, Inguinal_male_rna_2, Inguinal_female_protein_3, Inguinal_female_rna_4
from search.models import Perigonadal_male_protein_5, Perigonadal_male_rna_6, Perigonadal_female_protein_7, Perigonadal_female_rna_8
from search.models import Sex_fip_protein_9, Sex_fip_rna_10, Sex_apc_protein_11, Sex_apc_rna_12, Sex_dpp4_positive_protein_13, Sex_dpp4_positive_rna_14
from search.models import Sex_dpp4_neg_protein_15, Sex_dpp4_neg_rna_16, Depot_male_protein_17, Depot_male_rna_18, Depot_female_protein_19, Depot_female_rna_20
import os

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):

        Inguinal_male_protein_1.objects.all().delete()    
        Inguinal_male_rna_2.objects.all().delete()
        Inguinal_female_protein_3.objects.all().delete()
        Inguinal_female_rna_4.objects.all().delete()
        Perigonadal_male_protein_5.objects.all().delete()
        Perigonadal_male_rna_6.objects.all().delete()
        Perigonadal_female_protein_7.objects.all().delete()
        Perigonadal_female_rna_8.objects.all().delete()
        Sex_fip_protein_9.objects.all().delete()
        Sex_fip_rna_10.objects.all().delete()
        Sex_apc_protein_11.objects.all().delete()
        Sex_apc_rna_12.objects.all().delete()
        Sex_dpp4_positive_protein_13.objects.all().delete()
        Sex_dpp4_positive_rna_14.objects.all().delete()
        Sex_dpp4_neg_protein_15.objects.all().delete()
        Sex_dpp4_neg_rna_16.objects.all().delete()
        Depot_male_protein_17.objects.all().delete()
        Depot_male_rna_18.objects.all().delete()
        Depot_female_protein_19.objects.all().delete()
        Depot_female_rna_20.objects.all().delete()

                
                