from django import forms
from django.core.exceptions import ValidationError
from pandas import read_csv, to_numeric, to_datetime
from pandas.errors import ParserError


class ImportReadingsForm(forms.Form):
    attached_file = forms.FileField(
        label="Readings data",
        required=True,
        allow_empty_file=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "aria-describedby": "inputGroupFileAddon01",
                "aria-label": "Upload",
                "accept": ".csv",
            }
        ),
    )

    def clean_attached_file(self):
        file = self.cleaned_data.get("attached_file")

        if not file.name.endswith(".csv"):
            raise ValidationError("Only *.csv files are allowed for importing.")

        try:
            file_df = read_csv(file)
        except ParserError:
            raise ValidationError("The file could not be parsed as a CSV.")
        except Exception as e:
            raise ValidationError(f"An error occurred when reading the CSV file: {e}.")

        if "VALUE" not in file_df.columns:
            raise ValidationError("The CSV file must contain 'VALUE' column.")
        if "DATE" not in file_df.columns:
            raise ValidationError("The CSV file must contain 'DATE' column.")

        try:
            file_df["VALUE"] = to_numeric(file_df["VALUE"])
            file_df["DATE"] = to_datetime(file_df["DATE"])
        except Exception as ex:
            raise ValidationError(f"An error occurred when converting the data: {ex}.")

        file_df = file_df.sort_values(by="DATE")

        return file_df
