# Generated by Django 5.1.2 on 2024-10-25 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legallinkerapp', '0005_rename_advocate_advocate_user_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advocate',
            old_name='user',
            new_name='advocate',
        ),
    ]
