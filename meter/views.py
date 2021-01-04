from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from meter.models import Meter, MeterInfo
from .forms import CreateMeterForm


# Create your views here.


class IndexPage(View):
    def post(self, request):
        try:
            meter_name = request.POST.get('meter_name')
            meter_resource = request.POST.get('meter_resource')
            meter_unit = request.POST.get('meter_unit')
            new_meter = Meter.objects.create(name=meter_name, resource_type=meter_resource, unit=meter_unit)
            success = True
        except:
            success = False
        meters = Meter.objects.all().order_by('pk')
        return render(request, 'meter/index.html', {"meters": meters, 'success': success})

    def get(self, request):
        meters = Meter.objects.all().order_by('pk')
        return render(request, 'meter/index.html', {"meters": meters})


class MeterDetails(View):
    def get(self, request, pk):
        try:
            meter = Meter.objects.get(pk=pk)
        except Meter.DoesNotExist:
            return Http404
        return render(request, 'meter/meter_details.html', {"meter": meter})


class NewMeter(View):
    def get(self, request):
        form = CreateMeterForm()
        return render(request, 'meter/new_meter.html', {'form': form})
