# Generated by Django 5.1.2 on 2024-10-26 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legallinkerapp', '0006_rename_user_advocate_advocate'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
