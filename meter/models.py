from django.db import models


# Create your models here.
class Meter(models.Model):
    name = models.CharField(max_length=255, unique=True)
    resource_type = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    meter_csv_file = models.FileField(upload_to='meter_csv/', default=None)
