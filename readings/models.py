from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from django.db import models

from MetersMonitoring.enums import MetricPrefixEnum
from MetersMonitoring.settings import DATE_FORMAT
from meters.models import Meter
from tariffs.models import Tariff


class MeterReading(models.Model):
    id = models.AutoField(primary_key=True)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    reading = models.FloatField(null=False, blank=False)
    date = models.DateField(default=datetime.today, null=False, blank=False)

    @staticmethod
    def get_consumption_and_expenses_data(meter_id):
        queryset = MeterReading.objects.filter(meter__id=meter_id).order_by("date")

        prev_reading = None
        result = []

        for meter_reading in queryset:
            relative_value = (
                meter_reading.reading - prev_reading if prev_reading is not None else 0
            )

            tariff = (
                Tariff.objects.filter(
                    meter__id=meter_reading.meter.id, start_date__lte=meter_reading.date
                )
                .order_by("-start_date")
                .first()
            )

            expenses = 0
            if tariff:
                multiplier_relative_value = Decimal(
                    MetricPrefixEnum.from_index(
                        meter_reading.meter.metric_prefix
                    ).multiplier
                )
                multiplier_tariff = Decimal(
                    MetricPrefixEnum.from_index(tariff.metric_prefix).multiplier
                )

                relative_value_converted = (
                    Decimal(relative_value) * multiplier_relative_value
                )
                tariff_converted = Decimal(tariff.price) / multiplier_tariff

                expenses = Decimal(
                    relative_value_converted * tariff_converted
                ).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

            result.append(
                {
                    "id": meter_reading.id,
                    "date": meter_reading.date.strftime(DATE_FORMAT),
                    "absolute_reading": meter_reading.reading,
                    "relative_reading": relative_value,
                    "expenses": expenses,
                }
            )

            prev_reading = meter_reading.reading

        return result
