from django import forms


class DataFileForm(forms.Form):
    file = forms.FileInput()
