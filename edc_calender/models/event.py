from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('title')
        return fields

    class Meta:
        abstract = True


class ContactManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, mobile_number):
        return self.get(title='title')


class Event(
        SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    title = models.CharField(
        verbose_name='Event Title',
        max_length=200)
 
    description = models.TextField(
        verbose_name='Event description')

    start_time = models.DateTimeField(
        verbose_name='Start date and time')

    end_time = models.DateTimeField(
        verbose_name='End date and time')

    class Meta:
        app_label = "edc_calender"
