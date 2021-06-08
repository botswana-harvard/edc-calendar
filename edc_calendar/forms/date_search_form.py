from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class DateSearchForm(forms.Form):


    month = forms.DateField(
        required=True, label='Pick date',
        widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = 'date_search_report'
        self.helper.form_action = 'edc_calendar:home_url'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'month',
            Submit('submit', u'filter date', css_class="btn btn-sm btn-default center"),
        )