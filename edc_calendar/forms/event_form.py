from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import Event


class EventForm(SiteModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        fields = '__all__'
