from django.contrib import messages
from django.shortcuts import render, redirect

from common.views import BaseView
from meters.forms import CreateMeterForm
from meters.models import Meter
from readings.forms import ImportReadingsForm
from readings.models import MeterReading
from tariffs.forms import CreateTariffForm
from tariffs.models import Tariff


class MetersView(BaseView):
    def get(self, request):
        meters = [meter.to_dict() for meter in Meter.objects.all()]
        return render(
            request,
            "meters/index.html",
            {"meters": meters, "create_meter_form": CreateMeterForm()},
        )

    def post(self, request):
        form = CreateMeterForm(request.POST)

        if not form.is_valid():
            # Storing form error messages in list
            [
                messages.error(
                    request, f"'{form[field_slug].label}' field: {error_message}"
                )
                for field_slug, error_list in form.errors.items()
                for error_message in error_list
            ]
            return redirect("main")

        form_data = form.cleaned_data
        meter_name = form_data["name"].strip()

        if Meter.objects.filter(name=meter_name).exists():
            messages.error(
                request,
                f"'{form['name'].label}' field: Meter with '{meter_name}' name already exists.",
            )
            return redirect("main")

        Meter.objects.create(
            name=meter_name,
            resource=int(form_data["resource"]),
            metric_prefix=int(form_data["metric_prefix"]),
        )
        messages.success(request, f"Meter '{meter_name}' created successfully.")

        return redirect("main")


class MeterDetailsView(BaseView):
    def get(self, request, meter_id):
        meter_obj = Meter.objects.get(id=meter_id)

        data = {
            "meter": meter_obj.to_dict(),
            "tariffs": [
                tariff.to_dict() for tariff in Tariff.objects.filter(meter=meter_obj)
            ],
            "consumption_and_expenses_data": MeterReading.get_consumption_and_expenses_data(
                meter_obj.id
            ),
            "import_readings_form": ImportReadingsForm(),
            "create_tariff_form": CreateTariffForm(),
        }

        return render(request, "meters/meter_details.html", data)

    def patch(self, request, meter_id):
        form = CreateMeterForm(request.POST)

        if not form.is_valid():
            # Storing form error messages in list
            [
                messages.error(
                    request, f"'{form[field_slug].label}' field: {error_message}"
                )
                for field_slug, error_list in form.errors.items()
                for error_message in error_list
            ]
            return redirect("main")

        form_data = form.cleaned_data
        meter_name = form_data["name"].strip()

        meter_obj = Meter.objects.get(id=meter_id)

        if (
            Meter.objects.filter(name=meter_name).exists()
            and meter_obj.name != meter_name
        ):
            messages.error(
                request,
                f"'{form['name'].label}' field: Meter with '{meter_name}' name already exists.",
            )
            return redirect("main")

        meter_obj.name = meter_name
        meter_obj.resource = int(form_data["resource"])
        meter_obj.metric_prefix = int(form_data["metric_prefix"])
        meter_obj.save()

        messages.success(request, f"Meter '{meter_name}' updated successfully.")
        return redirect("main")

    def delete(self, request, meter_id):
        if not Meter.objects.filter(id=meter_id).exists():
            messages.error(request, f"Meter not found with the given id: '{meter_id}'.")
            return redirect("main")

        Meter.objects.get(id=meter_id).delete()
        messages.success(request, "Meter was deleted successfully.")

        return redirect("main")
