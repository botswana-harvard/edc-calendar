from django.db import models

from dateutil.relativedelta import weekday


class FacilityDayManager(models.Manager):

    def days(self, name):
        """Returns an ordered list of weekday objects for a given facility."""
        facility_days = super().get_queryset().filter(facility__name=name).order_by('facility_day')
        days = []
        for obj in facility_days:
            days.append(weekday(int(obj.facility_day)))
        return days
