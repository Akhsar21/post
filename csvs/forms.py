from django import forms
from .models import Csv


class CsvForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for field in self.Meta.required:
        #     self.fields[field].required = False

    class Meta:
        model = Csv
        fields = ("file_name", )
        # required = ("", )
        widget = {
            'file_name': forms.ClearableFileInput(attrs={})
        }
