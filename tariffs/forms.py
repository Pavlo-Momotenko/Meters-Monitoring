from datetime import date

from django import forms

from MetersMonitoring.settings import DATE_FORMAT
from meters.forms import MetricPrefixEnum
from tariffs.models import Tariff


class CreateTariffForm(forms.Form):
    model = Tariff
    name = forms.CharField(
        label="Tariff Name",
        min_length=3,
        max_length=60,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": "Meter name",
                "autocomplete": "off",
                "placeholder": "Main tariff",
            }
        ),
    )
    price = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        required=True,
        label="Price ($)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "aria-label": "Price",
                "autocomplete": "off",
                "placeholder": "2,50",
            }
        ),
    )
    metric_prefix = forms.ChoiceField(
        label="Metric Prefix",
        choices=[(choice.index, choice.description) for choice in MetricPrefixEnum],
        required=True,
        initial=MetricPrefixEnum.NONE.index,
        widget=forms.Select(
            attrs={"class": "form-control", "aria-label": "Metric Prefix"}
        ),
    )
    start_date = forms.DateField(
        input_formats=[DATE_FORMAT],
        required=True,
        label="Start Date",
        initial=date.today().strftime(DATE_FORMAT),
        widget=forms.DateInput(
            format=DATE_FORMAT,
            attrs={
                "class": "form-control",
                "aria-label": "Start Date",
                "autocomplete": "off",
                "placeholder": "dd/mm/yyyy",
            },
        ),
    )
