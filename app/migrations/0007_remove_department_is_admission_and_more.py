# Generated by Django 5.0.7 on 2024-07-16 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_diagnosis_examination_familymedicalhistory_finding_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='is_admission',
        ),
        migrations.RemoveField(
            model_name='department',
            name='is_pharmacy',
        ),
    ]