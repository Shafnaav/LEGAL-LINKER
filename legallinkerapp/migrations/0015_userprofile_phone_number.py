# Generated by Django 5.1.2 on 2024-11-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legallinkerapp', '0014_remove_advocate_location_delete_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
