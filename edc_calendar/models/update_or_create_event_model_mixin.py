from django.apps import apps as django_apps
from django.db import models

from .event import Event


class UpdatesOrCreatesCalenderEventModelError(Exception):
    pass


class UpdatesOrCreatesCalenderEventModelMixin(models.Model):

    """A model mixin that creates or updates a calender event
    on post_save signal.
    """

    def create_or_update_calender_event(self):
        """Creates or Updates the event model with attributes
        from this instance.
        Called from the signal
        """
        if not getattr(self, self.identifier_field) and not getattr(self, self.title_field):
            raise UpdatesOrCreatesCalenderEventModelError(
                f'Cannot update or create Calender Event. '
                f'Field value for \'{self.identifier_field}\' is None.')

        event_value = getattr(self, self.identifier_field)
        title_value = getattr(self, self.title_field)
        if getattr(self, self.second_title_field):
            title_value += str(getattr(self, self.second_title_field))
        try:
            Event.objects.get(**{
                self.identifier_field: event_value,
                'title': title_value})
        except Event.DoesNotExist:
            Event.objects.create(
                **{self.identifier_field: event_value, 'title': title_value},
                **self.event_options)


    @property
    def identifier_field(self):
        """Returns the field attr on YOUR model that will update
        `identifier_field`.
        """
        return 'subject_identifier'

    @property
    def title_field(self):
        """Returns the field attr on YOUR model that will update
        `title`.
        """
        return 'visit_code'

    @property
    def second_title_field(self):
        """Returns the field attr on YOUR model that will update
        `title`.
        """
        return 'visit_code_sequence'
        

    @property
    def event_options(self):
        """Returns the dict of the following attrs
        `description` `start_time`  `end_time`.
        """
        return {}


    class Meta:
        abstract = True