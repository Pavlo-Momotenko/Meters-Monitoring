from decimal import Decimal, ROUND_UP

from django.contrib import messages
from django.shortcuts import redirect

from common.views import BaseView
from meters.models import Meter
from tariffs.models import Tariff
from tariffs.forms import CreateTariffForm


class TariffsView(BaseView):
    def post(self, request, meter_id):
        form = CreateTariffForm(request.POST)

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

        form_data = form.cleaned_data
        tariff_name = form_data["name"].strip()

        if Tariff.objects.filter(meter__id=meter_id, name=tariff_name).exists():
            messages.error(
                request,
                f"'{form['name'].label}' field: Tariff with '{tariff_name}' name already exists.",
            )
            return redirect("meter_details", meter_id=meter_id)

        start_date = form_data["start_date"]
        if Tariff.objects.filter(meter__id=meter_id, start_date=start_date).exists():
            messages.error(
                request,
                f"'{form['start_date'].label}' field: Tariff with '{start_date}' start date already exists.",
            )
            return redirect("meter_details", meter_id=meter_id)

        Tariff.objects.create(
            name=tariff_name,
            meter=Meter.objects.get(id=meter_id),
            metric_prefix=int(form_data["metric_prefix"]),
            price=Decimal(form_data["price"]).quantize(
                Decimal(".01"), rounding=ROUND_UP
            ),
            start_date=start_date,
        )
        messages.success(request, f"Tariff '{tariff_name}' created successfully.")

        return redirect("meter_details", meter_id=meter_id)


class TariffDetailsView(BaseView):
    def patch(self, request, meter_id, tariff_id):
        form = CreateTariffForm(request.POST)

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

        form_data = form.cleaned_data
        tariff_name = form_data["name"].strip()
        tariff_obj = Tariff.objects.get(id=tariff_id)

        if (
            Tariff.objects.filter(meter__id=meter_id, name=tariff_name).exists()
            and tariff_obj.name != tariff_name
        ):
            messages.error(
                request,
                f"'{form['name'].label}' field: Tariff with '{tariff_name}' name already exists.",
            )
            return redirect("meter_details", meter_id=meter_id)

        start_date = form_data["start_date"]
        if (
            Tariff.objects.filter(meter__id=meter_id, start_date=start_date).exists()
            and tariff_obj.start_date != start_date
        ):
            messages.error(
                request,
                f"'{form['start_date'].label}' field: Tariff with '{start_date}' start date already exists.",
            )
            return redirect("meter_details", meter_id=meter_id)

        tariff_obj.name = tariff_name
        tariff_obj.metric_prefix = int(form_data["metric_prefix"])
        tariff_obj.price = Decimal(form_data["price"]).quantize(
            Decimal(".01"), rounding=ROUND_UP
        )
        tariff_obj.start_date = start_date
        tariff_obj.save()
        messages.success(request, f"Tariff '{tariff_name}' updated successfully.")

        return redirect("meter_details", meter_id=meter_id)

    def delete(self, request, meter_id, tariff_id):
        if not Tariff.objects.filter(id=tariff_id, meter__id=meter_id).exists():
            messages.error(
                request, f"Tariff not found with the given id: '{tariff_id}'."
            )
            return redirect("meter_details", meter_id=meter_id)

        Tariff.objects.get(id=tariff_id).delete()
        messages.success(request, "Tariff was deleted successfully.")

        return redirect("meter_details", meter_id=meter_id)
