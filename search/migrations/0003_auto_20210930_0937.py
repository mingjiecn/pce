# Generated by Django 3.2.6 on 2021-09-30 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20210930_0905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('CA19_9', 'CA19_9'), ('CEA', 'CEA'), ('CBC', 'CBC'), ('NEUTROPHIL', 'NEUTROPHIL')], max_length=20)),
                ('value', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.patient')),
            ],
            options={
                'verbose_name_plural': 'Lab',
            },
        ),
        migrations.DeleteModel(
            name='Ca_19_9',
        ),
    ]
