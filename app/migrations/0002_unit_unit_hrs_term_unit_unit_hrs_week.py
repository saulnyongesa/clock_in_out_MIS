# Generated by Django 5.0.7 on 2024-07-11 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='unit_hrs_term',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='unit_hrs_week',
            field=models.IntegerField(null=True),
        ),
    ]