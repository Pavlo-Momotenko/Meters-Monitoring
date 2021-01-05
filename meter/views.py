import operator

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from meter.models import Meter
import csv, datetime


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

            dates = dict()
            with open(file_path) as csv_file:
                for row in csv.reader(csv_file):
                    try:
                        date = row[0].split('-')
                        dates[datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))] = float(row[1])
                    except:
                        if row[1].isdigit():
                            dates['null'] = float(row[1])
                print(dates)
            x_axis = list()
            y_axis = list()
            sorted_dates = sorted(dates.items(), key=operator.itemgetter(0))
            print(sorted_dates)
            for i in sorted_dates:
                x_axis.append(str(i[0].day) + '/' + str(i[0].month) + '/' + str(i[0].year))
                y_axis.append(dates[i[0]])

            print(len(x_axis), len(y_axis))
            print(x_axis, y_axis)
            meter = Meter.objects.get(pk=pk)
        except Meter.DoesNotExist:
            return Http404
        return render(request, 'meter/meter_details.html',
                      {"meter": meter, 'pk': pk, 'last_reading_date': max(dates), 'last_reading': dates[max(dates)],
                       'x_axis': x_axis, 'y_axis': y_axis})

    def get(self, request, pk):
        try:
            meter = Meter.objects.get(pk=pk)
        except Meter.DoesNotExist:
            return Http404
        return render(request, 'meter/meter_details.html', {"meter": meter, 'pk': pk})


class NewMeter(View):
    def get(self, request):
        return render(request, 'meter/new_meter.html', {})
