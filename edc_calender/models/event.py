from django.db import models
from django.urls.base import reverse

from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base
from django.conf import settings


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('title')
        return fields

    class Meta:
        abstract = True


class ContactManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, mobile_number):
        return self.get(subject_identifier='subject_identifier')


class Event(
        SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    title = models.CharField(
        verbose_name='Event Title',
        max_length=200)
 
    description = models.TextField(
        verbose_name='Event description')

    start_time = models.DateTimeField(
        verbose_name='Start date and time')

    end_time = models.DateTimeField(
        verbose_name='End date and time')

    def __str__(self):
        return f'{self.subject_identifier} {self.title}'

    class Meta:
        app_label = "edc_calender"

    @property
    def get_html_url(self):
        dashboard_url = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
        url = reverse(f'{dashboard_url}', kwargs={'subject_identifier': self.subject_identifier})
        return f'<a href="{url}">{self.subject_identifier}: {self.title}</a>'
