from django import forms

from MetersMonitoring.enums import ResourceEnum, MetricPrefixEnum
from meters.models import Meter


class CreateMeterForm(forms.Form):
    model = Meter
    name = forms.CharField(
        label="Meter Name",
        min_length=3,
        max_length=60,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": "Meter name",
                "autocomplete": "off",
                "placeholder": "Hotel meter",
            }
        ),
    )
    resource = forms.ChoiceField(
        label="Resource",
        choices=[
            (choice.index, f"{choice.description} ({choice.code})")
            for choice in ResourceEnum
        ],
        required=True,
        initial=ResourceEnum.ELECTRICITY.index,
        widget=forms.Select(
            attrs={"class": "form-select", "arial-label": "Resource type"}
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
