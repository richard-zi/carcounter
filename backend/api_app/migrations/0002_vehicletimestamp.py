# Generated by Django 4.2.5 on 2023-09-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleTimestamp",
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
                    ),
                ),
                (
                    "direction",
                    models.CharField(
                        choices=[("in", "In"), ("out", "Out")], max_length=4
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]