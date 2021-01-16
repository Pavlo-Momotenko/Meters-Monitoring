import csv
import datetime
import operator
import os

from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from meter.forms import CreateMeterForm, DataFileUploadForm
from meter.models import Meter


# Create your views here.

class DataReadHelper:
    @staticmethod
    def get_date_from_string(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    @staticmethod
    def write_new_file_from_dictionary(file_path, dictionary):
        with open(str(file_path), 'w', newline='') as new_csv_file:
            field_names = ['DATE', 'VALUE']
            writer = csv.DictWriter(new_csv_file, field_names)
            writer.writeheader()

            for date, value in dictionary.items():
                writer.writerow({field_names[0]: date.strftime('%Y-%m-%d'), field_names[1]: value})

    def get_formatted_dict(self, dictionary):
        formatted_dict = dict()

        for data_row in dictionary:
            if 'DATE' in data_row and 'VALUE' in data_row:
                if data_row['DATE'] and data_row['VALUE']:
                    #ЗАПИЛИТЬ ТРАЙ ЕКСЕПТ
                    formatted_dict[self.get_date_from_string(data_row['DATE'])] = round(float(data_row['VALUE']), 1)
            else:
                break

        return formatted_dict

    @staticmethod
    def get_sorted_dictionary(dictionary):
        return dict(sorted(dictionary.items()))

    def get_data_from_file(self, file_path):
        x_y_axis_data = dict()

        if os.path.exists(str(file_path)):
            with open(str(file_path), 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                x_y_axis_data = self.get_formatted_dict(reader)

        return x_y_axis_data

    def post_data_for_page(self, file, file_path):
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        sorted_data_in_existed_meter = dict()

        if os.path.exists(str(file_path)):
            sorted_data_in_existed_meter = self.get_data_from_file(file_path)

        new_data_for_existed_meter = self.get_formatted_dict(reader)

        new_data = dict()
        new_data.update(sorted_data_in_existed_meter)
        new_data.update(new_data_for_existed_meter)

        self.write_new_file_from_dictionary(file_path, new_data)

    def get_data_for_page(self, file_path):
        x_y_axis_data, last_reading_date, last_reading = dict(), None, None
        x_y_axis_data = self.get_data_from_file(file_path)

        if len(x_y_axis_data) > 0:
            x_y_axis_data = self.get_sorted_dictionary(x_y_axis_data)
            last_reading_date = max(x_y_axis_data)
            last_reading = x_y_axis_data[last_reading_date]

        return x_y_axis_data, last_reading_date, last_reading


class IndexPage(View):
    @staticmethod
    def post(request):
        new_meter_form = CreateMeterForm(request.POST)
        meters = Meter.objects

        if new_meter_form.is_valid():
            data = new_meter_form.cleaned_data
            is_name_in_database = meters.filter(name=data['name']).count()

            if not is_name_in_database:
                meters.create(name=data['name'], resource_type=data['resource'], unit=data['unit'])

            request.session['success'] = False if is_name_in_database else True

        if request.POST.get('delete_meter'):
            primary_key = int(request.POST.get('delete_meter'))
            is_pk_in_database = meters.filter(pk=primary_key)

            if os.path.exists(f"meter_csv/{primary_key}.csv"):
                os.remove(f"meter_csv/{primary_key}.csv")
                meters.get(pk=primary_key).meter_csv_file.delete()

            if is_pk_in_database:
                meters.get(pk=primary_key).delete()

        return redirect(request.path)

    @staticmethod
    def get(request):
        success = request.session.get('success', None)
        all_meters = Meter.objects.all()

        if success is not None:
            del (request.session['success'])

        return render(request, 'meter/index.html', {"meters": all_meters, "success": success})


class MeterDetails(View, DataReadHelper):
    def post(self, request, pk):
        file_upload_form = DataFileUploadForm(request.POST, request.FILES)

        meters = Meter.objects
        is_pk_in_database = meters.filter(pk=pk)

        if request.POST.get('reset_meter'):
            if os.path.exists(f'meter_csv/{pk}.csv'):
                os.remove(f'meter_csv/{pk}.csv')

            if is_pk_in_database:
                meters.get(pk=pk).meter_csv_file.delete()

            return redirect(request.path)

        if file_upload_form.is_valid():
            file = file_upload_form.cleaned_data['file']

            if file.name[-4:] == '.csv':
                file.name = f"{pk}.csv"
            else:
                file_upload_form.add_error('file', 'File extension is incorrect, it must have .csv extension!')
                request.session['file_upload_form'] = file_upload_form.errors.as_text().split('*')[2:]
                return redirect(request.path)

            if is_pk_in_database:
                file_path = meters.get(pk=pk).meter_csv_file

                if file_path:
                    self.post_data_for_page(file, file_path)
                else:
                    meter_without_file = meters.get(pk=pk)
                    meter_without_file.meter_csv_file = file
                    meter_without_file.save()
        else:
            request.session['file_upload_form'] = file_upload_form.errors.as_text().split('*')[2:]
            return redirect(request.path)

        return redirect(request.path)

    def get(self, request, pk):
        errors = request.session.get('file_upload_form', None)
        file_upload_form = DataFileUploadForm()

        meters = Meter.objects
        is_pk_in_database = meters.filter(pk=pk)

        last_reading_date, last_reading = None, None
        x_y_axis_data = dict()

        if errors is not None:
            del (request.session['file_upload_form'])

        if is_pk_in_database:
            meter_file_path = meters.get(pk=pk).meter_csv_file or None
            if meter_file_path:
                x_y_axis_data, last_reading_date, last_reading = self.get_data_for_page(meter_file_path)
        else:
            raise Http404

        return render(request, 'meter/meter_details.html',
                      {"meter": meters.get(pk=pk), 'pk': pk, 'last_reading_date': last_reading_date,
                       'last_reading': last_reading, 'x_axis': list(x_y_axis_data.keys()),
                       'y_axis': list(x_y_axis_data.values()), 'file_upload_form': file_upload_form, 'errors': errors})


class NewMeter(View):
    @staticmethod
    def get(request):
        new_meter_form = CreateMeterForm()
        return render(request, 'meter/new_meter.html', {'new_meter_form': new_meter_form})
