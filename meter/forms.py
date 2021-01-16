from django import forms


class CreateMeterForm(forms.Form):
    CHOICES = (
        ('Electricity', 'Electricity'),
        ('Water', 'Water'),
        ('Gas', 'Gas'),
    )
    name = forms.CharField(label='Meter Name', min_length=3, max_length=60,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Meter name'}))
    resource = forms.ChoiceField(label='Resource', choices=CHOICES, required=True,
                                 widget=forms.Select(attrs={'class': 'form-select', 'arial-label': 'Resource type'}))
    unit = forms.CharField(label='Unit', max_length=20, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Unit'}))


class DataFileUploadForm(forms.Form):
    file = forms.FileField(required=True, allow_empty_file=False,  widget=forms.FileInput(
        attrs={'class': 'form-control', 'aria-describedby': 'inputGroupFileAddon01',
               'aria-label': 'Upload'}))
