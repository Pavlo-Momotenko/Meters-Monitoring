from datetime import date

from django.contrib import messages
from django.shortcuts import redirect
from pandas import DataFrame, isnull, to_datetime, to_numeric

from common.views import BaseView
from meters.models import Meter
from readings.forms import ImportReadingsForm
from readings.models import MeterReading


class ReadingsView(BaseView):
    def post(self, request, meter_id):
        form = ImportReadingsForm(request.POST, request.FILES)

        if not form.is_valid():
            # Storing form error messages in list
            [
                messages.error(
                    request, f"'{form[field_slug].label}' field: {error_message}"
                )
                for field_slug, error_list in form.errors.items()
                for error_message in error_list
            ]
            return redirect("meter_details", meter_id=meter_id)

        imported_meter_readings = form.cleaned_data.get("attached_file")

        meter = Meter.objects.get(id=meter_id)

        meter_readings = DataFrame.from_records(
            MeterReading.objects.filter(meter=meter).values(),
            columns=[field.name for field in MeterReading._meta.get_fields()],
        )
        meter_readings["date"] = to_datetime(meter_readings["date"])
        meter_readings["reading"] = to_numeric(meter_readings["reading"])

        count = 0
        for index, row in imported_meter_readings.iterrows():
            if isnull(row["DATE"]) or isnull(row["VALUE"]):
                messages.error(
                    request, f"Row {index + 1}: Empty values are not allowed."
                )
                continue

            if row["DATE"].date() > date.today():
                messages.error(
                    request, f"Row {index + 1}: Date cannot be in the future."
                )
                continue

            if row["VALUE"] < 0:
                messages.error(
                    request, f"Row {index + 1}: Unsigned value allowed only."
                )
                continue

            temp_meter_reading = meter_readings[["date", "reading"]].copy()
            idx = temp_meter_reading[temp_meter_reading["date"] == row["DATE"]].index
            temp_meter_reading.loc[
                len(temp_meter_reading.index) if idx.empty else idx
            ] = [row["DATE"], row["VALUE"]]
            temp_meter_reading = temp_meter_reading.sort_values(by="date")

            if not temp_meter_reading["reading"].equals(
                temp_meter_reading["reading"].sort_values()
            ):
                messages.error(
                    request, f"Row {index + 1}: Readings are not in increasing order."
                )
                continue

            MeterReading.objects.update_or_create(
                meter=meter,
                date=row["DATE"],
                defaults={"reading": row["VALUE"], "date": row["DATE"]},
            )

            count += 1
            meter_readings = temp_meter_reading

        if count:
            messages.success(request, f"{count} readings imported successfully.")

        return redirect("meter_details", meter_id=meter_id)

    def delete(self, request, meter_id):
        meter_readings = MeterReading.objects.filter(meter__id=meter_id)
        if not meter_readings.exists():
            messages.error(
                request,
                f"Meter readings not found with the given meter id: '{meter_id}'.",
            )
            return redirect("meter_details", meter_id=meter_id)

        meter_readings.delete()
        messages.success(request, "Meter readings were deleted successfully.")

        return redirect("meter_details", meter_id=meter_id)
