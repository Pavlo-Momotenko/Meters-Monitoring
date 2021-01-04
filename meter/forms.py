from django import forms


class CreateMeterForm(forms.Form):
    meter_name = forms.CharField(label='Meter name', max_length=255, min_length=3)
