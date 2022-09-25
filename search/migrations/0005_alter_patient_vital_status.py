# Generated by Django 3.2.6 on 2021-10-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_patient_vital_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='vital_status',
            field=models.CharField(choices=[('Dead', 'Dead'), ('Alive', 'Alive')], max_length=20, null=True),
        ),
    ]