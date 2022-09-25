from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class Patient(models.Model):
    uuid = models.CharField(max_length=36)
    accession = models.CharField(max_length=8)
    class Sex(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')
	
    sex = models.CharField(
        max_length=6,
        choices=Sex.choices,
    )

    class VitalStatus(models.TextChoices):
        DEAD = 'Dead', _('Dead')
        ALIVE = 'Alive', _('Alive')
	
    vital_status = models.CharField(
        null=True,
        max_length=20,
        choices=VitalStatus.choices,
    )

    date_of_death = models.DateField(null=True)
    last_follow_up = models.DateField(null=True)
    date_of_diagnosis = models.DateField(null=True)
    age_at_diagnosis = models.IntegerField(null=True, validators = [MinValueValidator(0), MaxValueValidator(200)])



    class Category(models.TextChoices):
        NA_SABR = 'NA SABR', _('NA SABR')
        NA_Chemo = 'NA Chemo only', _('NA Chemo only')
        Upfront_Surgery = 'Upfront surgery', _('Upfront surgery')
        Stage_4 = 'Stage 4', _('Stage 4')
	
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        null=True,
    )

    
    def __str__(self):
        return self.accession

    class Meta:
        verbose_name_plural = "Patients"

class Pathology_TR(models.Model):
    date_of_surgery = models.DateField(null=True)
    date_of_diagnosis = models.DateField()
    age_at_diagnosis = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(200)])
    class NodeCategory(models.TextChoices):
        NEGATIVE = '00 All nodes examined are negative', _('00 All nodes examined are negative')
        P1 = '1', _('1')
        P2 = '2', _('2')
        P3 = '3', _('3')
        P4 = '4', _('4')
        P5 = '5', _('5')
        P6 = '6', _('6')
        P7 = '7', _('7')
        P8 = '8', _('8')
        P9 = '9', _('9')
        P10 = '10', _('10')
        P11 = '11', _('11')
        P12 = '12', _('12')
        P13 = '13', _('13')
        P14 = '14', _('14')
        P15 = '15', _('15')
        NA = '98 No nodes were examined', _('98 No nodes were examined')
    node_category = models.CharField(
        max_length=100,
        choices=NodeCategory.choices,
    )
    #positive_node_number = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(20)])
    class LymphVascularInvasion(models.TextChoices):
        NEGATIVE = '0 Lymph-vascular Invasion stated as Not Present', _('0 Lymph-vascular Invasion stated as Not Present')
        POSITIVE = '1 Lymph-vascular Invasion Present/Identified', _('1 Lymph-vascular Invasion Present/Identified')
        NA = '9 Unknown/Indeterminate/not mentioned in path report', _('9 Unknown/Indeterminate/not mentioned in path report')
    lymph_vascular_invasion = models.CharField(
        null=True,
        max_length=130,
        choices=LymphVascularInvasion.choices,
    )
    class TumorGrade(models.TextChoices):
        I = '1 Grade I', _('1 Grade I')
        II = '2 Grade II', _('2 Grade II')
        III = '3 Grade III', _('3 Grade III')
        IV = '4 Grade IV', _('4 Grade IV')
        VI = '6 B-cell', _('6 B-cell')
        NA = '9 Grade/differentiation unknown, not stated, or not applicable', _('9 Grade/differentiation unknown, not stated, or not applicable')
    tumor_grade = models.CharField(
        null=True,
        max_length=70,
        choices=TumorGrade.choices,
    )
    class SurgicalMargin(models.TextChoices):
        NEGATIVE = '0 No residual tumor', _('0 No residual tumor')
        POSITIVE = '1 Residual tumor, NOS', _('1 Residual tumor, NOS')
        MICROSCOPIC = '2 Microscopic residual tumor', _('2 Microscopic residual tumor')
        MACROSCOPIC = '3 Macroscopic residual tumor', _('3 Macroscopic residual tumor')
        NON_EVALUABLE = '7 Margins not evaluable', _('7 Margins not evaluable')
        NO_PRIMARY_SITE = '8 No primary site surgery', _('8 No primary site surgery')
        UNKNOWN = '9 Unknown or not applicable', _('9 Unknown or not applicable')

        
    surgical_margin = models.CharField(
        max_length=30,
        choices=SurgicalMargin.choices,
    )

    location_of_tumor = models.CharField(max_length=50)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)
    class Meta:
        verbose_name_plural = "Pathology"
    def __str__(self):
        return self.patient.accession
    

class Procedure(models.Model):
    date = models.DateField()
    class TypeOfSurgery(models.TextChoices):
        WHIPPLE = 'Pancreaticoduodenectomy (Whipple resection), partial pancreatectomy', _('Pancreaticoduodenectomy (Whipple resection), partial pancreatectomy')
        OTHER = 'Other (specify)', _('Other (specify)')

    type_of_surgery =  models.CharField(
        max_length=80,
        choices=TypeOfSurgery.choices,
    )
    class PeriNeuralInvasion(models.TextChoices):
        NEGATIVE = 'Not identified', _('Not identified')
        POSITIVE = 'Present', _('Present')
    peri_neural_invasion = models.CharField(
        max_length=20,
        choices=PeriNeuralInvasion.choices,
    )
    
    pathological_response = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(2)],null=True,)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = "Procedure"
    def __str__(self):
        return self.patient.accession + '_' + str(self.date)

class Lab(models.Model):
    class Name(models.TextChoices):
        CA19_9 = 'CA19_9', _('CA19_9')
        CEA = 'CEA', _('CEA')
        CBC = 'CBC', _('CBC')
        NEUTROPHIL  = 'NEUTROPHIL', _('NEUTROPHIL')
       
    name = models.CharField(
        
        max_length=20,
        choices=Name.choices,
    )

    value = models.CharField(max_length=10)
    date = models.DateField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)
    class Meta:
        verbose_name_plural = "Lab"
    def __str__(self):
        return self.patient.accession + '_' + str(self.date)+ '_' + self.name
class RadiationSet(models.Model):
    set_id = models.IntegerField(validators = [MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)
    doses = models.IntegerField(validators = [MinValueValidator(1)])
    fractions = models.IntegerField(validators = [MinValueValidator(1)])
    site_name  = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = "Radiation Set"
    def __str__(self):
        return str(self.set_id)
class RadiationFraction(models.Model):
    doses = models.IntegerField(validators = [MinValueValidator(1)])
    fractions = models.IntegerField(validators = [MinValueValidator(1)])
    start_date = models.DateField()
    end_date = models.DateField()
    
    site_name  = models.CharField(max_length=30)
    days_elapsed = models.IntegerField(validators = [MinValueValidator(0)])

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)
    radiation_set = models.ForeignKey('RadiationSet', on_delete=models.CASCADE, null=False)
    
    class Meta:
        verbose_name_plural = "Radiation Fraction"
    def __str__(self):
        return self.patient.accession + '_' + str(self.start_date)

class ChemoPlan(models.Model):
    plan_id = models.IntegerField(validators = [MinValueValidator(0)])
    plan = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)
    number_of_cycle = models.IntegerField(validators = [MinValueValidator(1)])
    
    class Meta:
        verbose_name_plural = "Chemo Plan"
    def __str__(self):
        return str(self.plan_id)


class ChemoCycle(models.Model):
    class CycleStatus(models.TextChoices):
        COMPLETED = 'Completed', _('Completed')
        STARTED = 'Started', _('Started')
    protocol = models.CharField(max_length=200)
    start_date = models.DateField()
    cycle_number = models.IntegerField(validators = [MinValueValidator(0)])
    cycle_status = models.CharField(
        max_length=200,
        choices=CycleStatus.choices
    )
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=False)
    chemo_plan = models.ForeignKey('ChemoPlan', on_delete=models.CASCADE, null=False)
    class Meta:
        verbose_name_plural = "Chemo Cycle"
    def __str__(self):
        return self.patient.accession + '_' + str(self.start_date)

    
