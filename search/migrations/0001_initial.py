# Generated by Django 3.2.6 on 2021-09-29 15:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mrn', models.CharField(max_length=10)),
                ('sex', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6)),
                ('date_of_death', models.DateField(null=True)),
                ('last_follow_up', models.DateField(null=True)),
                ('date_of_diagnosis', models.DateField(null=True)),
                ('age_at_diagnosis', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)])),
                ('category', models.CharField(choices=[('NA SABR', 'NA SABR'), ('NA Chemo only', 'NA Chemo only'), ('Upfront surgery', 'Upfront surgery'), ('Stage 4', 'Stage 4')], max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Patients',
            },
        ),
        migrations.CreateModel(
            name='RadiationSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_id', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('doses', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fractions', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('site_name', models.CharField(max_length=30)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'Radiation Set',
            },
        ),
        migrations.CreateModel(
            name='RadiationFraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doses', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fractions', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('site_name', models.CharField(max_length=30)),
                ('days_elapsed', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
                ('radiation_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.radiationset')),
            ],
            options={
                'verbose_name_plural': 'Radiation Fraction',
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type_of_surgery', models.CharField(choices=[('Pancreaticoduodenectomy (Whipple resection), partial pancreatectomy', 'Pancreaticoduodenectomy (Whipple resection), partial pancreatectomy'), ('Other (specify)', 'Other (specify)')], max_length=80)),
                ('peri_neural_invasion', models.CharField(choices=[('Not identified', 'Not identified'), ('Present', 'Present')], max_length=20)),
                ('pathological_response', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'Procedure',
            },
        ),
        migrations.CreateModel(
            name='Pathology_TR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_surgery', models.DateField(null=True)),
                ('date_of_diagnosis', models.DateField()),
                ('age_at_diagnosis', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)])),
                ('node_category', models.CharField(choices=[('00 All nodes examined are negative', '00 All nodes examined are negative'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('98 No nodes were examined', '98 No nodes were examined')], max_length=100)),
                ('lymph_vascular_invasion', models.CharField(choices=[('0 Lymph-vascular Invasion stated as Not Present', '0 Lymph-vascular Invasion stated as Not Present'), ('1 Lymph-vascular Invasion Present/Identified', '1 Lymph-vascular Invasion Present/Identified'), ('9 Unknown/Indeterminate/not mentioned in path report', '9 Unknown/Indeterminate/not mentioned in path report')], max_length=130, null=True)),
                ('tumor_grade', models.CharField(choices=[('1 Grade I', '1 Grade I'), ('2 Grade II', '2 Grade II'), ('3 Grade III', '3 Grade III'), ('9 Grade/differentiation unknown, not stated, or not applicable', '9 Grade/differentiation unknown, not stated, or not applicable')], max_length=70, null=True)),
                ('surgical_margin', models.CharField(choices=[('0 No residual tumor', '0 No residual tumor'), ('1 Residual tumor, NOS', '1 Residual tumor, NOS'), ('8 No primary site surgery', '8 No primary site surgery')], max_length=30)),
                ('location_of_tumor', models.CharField(max_length=50)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'Pathology',
            },
        ),
        migrations.CreateModel(
            name='ChemoPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('plan', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('number_of_cycle', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'Chemo Plan',
            },
        ),
        migrations.CreateModel(
            name='ChemoCycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('cycle_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('cycle_status', models.CharField(choices=[('Completed', 'Completed'), ('Started', 'Started')], max_length=200)),
                ('chemo_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.chemoplan')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'Chemo Cycle',
            },
        ),
        migrations.CreateModel(
            name='Ca_19_9',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'CA 19-9',
            },
        ),
    ]
