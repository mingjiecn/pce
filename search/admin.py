from django.contrib import admin
from search.models import Patient, Pathology_TR, RadiationFraction, RadiationSet, Lab, ChemoCycle, ChemoPlan, Procedure



class Patient_admin(admin.ModelAdmin):
     list_display  = ('accession', 'category', 'sex', 'date_of_diagnosis', 'age_at_diagnosis','last_follow_up', 'date_of_death', 'vital_status')
     list_filter = ('category', 'sex','age_at_diagnosis' ,'vital_status',)
     search_fields = ["accession"]

class Pathology_TR_admin(admin.ModelAdmin):
     list_display  = ('patient', 'date_of_diagnosis', 'age_at_diagnosis','date_of_surgery', 'location_of_tumor', 'tumor_grade', 'surgical_margin', 'lymph_vascular_invasion', 'node_category')
     list_filter = ('location_of_tumor', 'lymph_vascular_invasion','tumor_grade', 'surgical_margin', 'node_category', 'age_at_diagnosis',)
     search_fields = ["patient__accession"]

class Procedure_admin(admin.ModelAdmin):
     list_display  = ('patient','date', 'type_of_surgery', 'peri_neural_invasion', 'pathological_response')
     list_filter = ('type_of_surgery', 'peri_neural_invasion','pathological_response' ,)
     search_fields = ["patient__accession"]

class RadiationFraction_admin(admin.ModelAdmin):
     list_display  = ('patient', 'doses', 'fractions','site_name', 'days_elapsed', 'start_date', 'end_date')
     list_filter = ('doses', 'fractions', 'site_name', )
     search_fields = ["patient__accession"]

class RadiationSet_admin(admin.ModelAdmin):
     list_display  = ('patient', 'doses', 'fractions','site_name', 'start_date', 'end_date')
     list_filter = ('doses', 'fractions', 'site_name',)
     search_fields = ["patient__accession"]


class Lab_admin(admin.ModelAdmin):
     list_display  = ('patient', 'name','value', 'date')
     list_filter = ('name',)
     search_fields = ["patient__accession"]

class ChemoCycle_admin(admin.ModelAdmin):
     list_display  = ('patient', 'chemo_plan', 'protocol', 'start_date', 'cycle_number', 'cycle_status')
     search_fields = ["patient__accession", "chemo_plan__plan_id"]
     list_filter = ('cycle_status', 'protocol',)

class ChemoPlan_admin(admin.ModelAdmin):
     list_display  = ('patient', 'plan_id', 'plan', 'start_date', 'end_date', 'number_of_cycle')
     search_fields = ["patient__accession"]
     list_filter = ('plan', 'number_of_cycle',)



admin.site.register(Patient, Patient_admin)
admin.site.register(Procedure, Procedure_admin)
admin.site.register(Pathology_TR, Pathology_TR_admin)
admin.site.register(RadiationFraction, RadiationFraction_admin)
admin.site.register(RadiationSet, RadiationSet_admin)
admin.site.register(Lab, Lab_admin)
admin.site.register(ChemoCycle, ChemoCycle_admin)
admin.site.register(ChemoPlan, ChemoPlan_admin)