from django.db import models

class VehicleData(models.Model):
    VEHICLE_CHOICES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('bus', 'Bus'),
    ]

    DIRECTION_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
    ]

    vehicle = models.CharField(max_length=10, choices=VEHICLE_CHOICES, verbose_name="Vehicle Type")
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, verbose_name="Direction")
    timestamp = models.DateTimeField(verbose_name="Timestamp")

    def __str__(self):
        return f"{self.vehicle} - {self.direction} - {self.timestamp}"

    class Meta:
        verbose_name = "Vehicle Data"
        verbose_name_plural = "Vehicle Data"