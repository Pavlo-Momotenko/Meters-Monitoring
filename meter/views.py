import csv
import datetime
import operator
from django.core.files import File

from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from meter.models import Meter


# Create your views here.

class DataReadHelper:
    def __init__(self, file_path, file=None):
        self.file_path = file_path
        self.file = file

    def get_ordered_value_and_key_from_existing_csv(self):
        dates = dict()
        x_axis = list()
        y_axis = list()
        file_path = self.file_path

        if file_path:
            with open(file_path) as csv_file:
                for row in csv.reader(csv_file):
                    try:
                        date = row[0].split('-')
                        dates[datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))] = float(row[1])
                    except:
                        if row[1].isdigit():
                            dates['null'] = float(row[1])

            sorted_dates = sorted(dates.items(), key=operator.itemgetter(0))
            for i in sorted_dates:
                x_axis.append(('0' if len(str(i[0].day)) < 2 else '') + str(i[0].day) + '/' + (
                    '0' if len(str(i[0].month)) < 2 else '') + str(i[0].month) + '/' + str(i[0].year))
                y_axis.append(dates[i[0]])

        return x_axis, y_axis, dates


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
                # with open(file_path, 'r') as file:

                print('yes', file_path)
            else:
                meter.meter_csv_file = file
                meter.save()
                file_path = str(meter.meter_csv_file)
                print('no', file_path)
        except Meter.DoesNotExist:
            return Http404
        return redirect(request.path)

    def get(self, request, pk):
        try:
            meter = Meter.objects.get(pk=pk)
            file_path = str(meter.meter_csv_file)

            last_reading_date = None
            last_reading = None
            x_axis = list()
            y_axis = list()

            if file_path:
                helper = DataReadHelper(file_path=file_path)
                x_axis, y_axis, dates = helper.get_ordered_value_and_key_from_existing_csv()

                last_reading_date = max(dates)
                last_reading = dates[max(dates)]
        except Meter.DoesNotExist:
            return Http404
        return render(request, 'meter/meter_details.html',
                      {"meter": meter, 'pk': pk, 'last_reading_date': last_reading_date, 'last_reading': last_reading,
                       'x_axis': x_axis, 'y_axis': y_axis})


class NewMeter(View):
    def get(self, request):
        return render(request, 'meter/new_meter.html', {})
