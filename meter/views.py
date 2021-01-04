from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from meter.models import Meter
import csv


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
    def post(self, request, pk):
        try:
            file = request.FILES.get('meter_file')
            file.name = f"{pk}.csv"
            meter = Meter.objects.get(pk=pk)
            if meter.meter_csv_file:
                file_path = str(meter.meter_csv_file)
                print('yes', file_path)
            else:
                meter.meter_csv_file = file
                meter.save()
                file_path = str(meter.meter_csv_file)
                print('no', file_path)

            print(str(file))
            # with open(file) as csv_file:
            #     spamreader = csv.reader(csv_file)
            #     for row in spamreader:
            #         print(', '.join(row))

            meter = Meter.objects.get(pk=pk)
        except Meter.DoesNotExist:
            return Http404
        return render(request, 'meter/meter_details.html', {"meter": meter, 'pk': pk})

    def get(self, request, pk):
        try:
            meter = Meter.objects.get(pk=pk)
        except Meter.DoesNotExist:
            return Http404
        return render(request, 'meter/meter_details.html', {"meter": meter, 'pk': pk})


class NewMeter(View):
    def get(self, request):
        return render(request, 'meter/new_meter.html', {})
