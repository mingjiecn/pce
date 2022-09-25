  
import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class PatientFilter(django_filters.FilterSet):

	class Meta:
		model = Patient
		fields = {
            'sex':['exact'],
            'category':['exact'],
            'age_at_diagnosis': ['lt', 'gt'],
            'date_of_diagnosis': ['year__exact'],
            'date_of_death': ['exact', 'year__gt'],
            
        }

class Pathology_TR_Filter(django_filters.FilterSet):

	class Meta:
		model = Pathology_TR
		fields = {
            'patient__accession':['exact'],
            'age_at_diagnosis': ['lt', 'gt'],
            'location_of_tumor':['exact'],
            'node_category':['exact'],
            'lymph_vascular_invasion':['exact'],
            'tumor_grade':['exact'],
            'surgical_margin':['exact'],
            
        }