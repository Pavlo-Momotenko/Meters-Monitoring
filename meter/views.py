from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from meter.models import Meter
from .forms import CreateMeterForm


# Create your views here.


class IndexPage(View):
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
