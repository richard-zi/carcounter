# Generated by Django 4.2.5 on 2023-09-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0004_rename_vehicle_vehicletimestamp_vehicle_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "vehicle",
                    models.CharField(
                        choices=[("car", "Car"), ("truck", "Truck"), ("bus", "Bus")],
                        max_length=10,
                        verbose_name="Vehicle Type",
                    ),
                ),
                (
                    "direction",
                    models.CharField(
                        choices=[("in", "In"), ("out", "Out")],
                        max_length=5,
                        verbose_name="Direction",
                    ),
                ),
                ("timestamp", models.DateTimeField(verbose_name="Timestamp")),
            ],
            options={
                "verbose_name": "Vehicle Data",
                "verbose_name_plural": "Vehicle Data",
            },
        ),
        migrations.DeleteModel(
            name="Data",
        ),
        migrations.DeleteModel(
            name="VehicleTimestamp",
        ),
    ]