# Generated by Django 4.2.5 on 2023-09-12 13:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0003_alter_vehicletimestamp_direction"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vehicletimestamp",
            old_name="vehicle",
            new_name="vehicle_type",
        ),
    ]
