from datetime import datetime

from django.db import models

from MetersMonitoring.enums import MetricPrefixEnum, ResourceEnum
from MetersMonitoring.settings import DATE_FORMAT
from meters.models import Meter


class Tariff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    metric_prefix = models.SmallIntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    start_date = models.DateField(default=datetime.today, null=False, blank=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit": MetricPrefixEnum.from_index(self.metric_prefix).code
            + ResourceEnum.from_index(self.meter.resource).code,
            "price": self.price,
            "start_date": self.start_date.strftime(DATE_FORMAT),
        }
