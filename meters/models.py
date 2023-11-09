from django.db import models

from MetersMonitoring.enums import ResourceEnum, MetricPrefixEnum


class Meter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    resource = models.SmallIntegerField(null=False, blank=False)
    metric_prefix = models.SmallIntegerField(null=False, blank=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "resource": ResourceEnum.from_index(self.resource).description,
            "unit": MetricPrefixEnum.from_index(self.metric_prefix).code
            + ResourceEnum.from_index(self.resource).code,
        }
