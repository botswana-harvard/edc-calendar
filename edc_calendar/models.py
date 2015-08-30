from django.db import models

from dateutil.relativedelta import weekday
from edc_calendar.managers import FacilityDayManager


DAYS = (
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)


class Holiday(models.Model):

    name = models.CharField(
        max_length=25)

    date = models.DateField(
        unique=True)

    def __str__(self):
        return '{} on {}'.format(self.name, self.date.strftime('%Y-%m-%d'))

    class Meta:
        ordering = ['date', ]
        app_label = 'edc_calendar'


class Facility(models.Model):

    name = models.CharField(
        max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'Facilities'
        app_label = 'edc_calendar'


class FacilityDay(models.Model):

    facility = models.ForeignKey(Facility)

    facility_day = models.CharField(
        verbose_name='Day',
        max_length=1,
        choices=DAYS,
    )

    appointments_per_day = models.IntegerField(
        null=True,
        blank=True,
        help_text='Maximum number of appointments allowed per day. Unlimited if left blank.')

    objects = FacilityDayManager()

    def __str__(self):
        return '{}'.format(self.facility)

    @property
    def day(self):
        return weekday(int(self.facility_day))

    class Meta:
        ordering = ['facility', 'facility_day']
        app_label = 'edc_calendar'
        unique_together = (('facility', 'facility_day'), )
