# Generated by Django 3.2.6 on 2022-10-09 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_auto_20220925_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='mrn',
        ),
    ]