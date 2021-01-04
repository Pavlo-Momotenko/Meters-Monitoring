from django import forms


class CreateMeterForm(forms.Form):
    meter_name = forms.CharField(label='Meter name', max_length=255, min_length=3)
    resource = forms.CharField(label='Resource', max_length=255, min_length=3)
    unit = forms.CharField(label='Unit', max_length=255, min_length=3)
