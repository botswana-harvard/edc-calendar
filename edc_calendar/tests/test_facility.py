import pytz

from datetime import datetime, timedelta
from django.db import models
from django.test import TestCase
from django.conf import settings
from dateutil.relativedelta import MO, WE, FR, relativedelta, weekday
from edc_calendar.models import FacilityDay, Facility, Holiday
from edc_calendar import Calendar

tz = pytz.timezone(settings.TIME_ZONE)


class Appointment(models.Model):

    subject = models.CharField(max_length=10)

    appt_datetime = models.DateTimeField()

    facility = models.ForeignKey(Facility)

    class Meta:
        app_label = 'edc_calendar'


class TestFacility(TestCase):

    def test_facility_day(self):
        facility = Facility.objects.create(name='gumare clinic')
        facility_day = FacilityDay.objects.create(
            facility=facility,
            facility_day='0',
        )
        facility_day = FacilityDay.objects.get(pk=facility_day.pk)
        self.assertEqual(facility_day.day, MO)

    def test_facility_manager(self):
        facility = Facility.objects.create(name='gumare clinic')
        for week_number in [0, 2, 4]:
            FacilityDay.objects.create(
                facility=facility,
                facility_day=week_number,
            )
        self.assertEqual(FacilityDay.objects.days(facility.name), [MO, WE, FR])

    def test_calendar_for_facility(self):
        facility = Facility.objects.create(name='gumare clinic')
        for week_number in [0, 2, 4]:
            FacilityDay.objects.create(
                facility=facility,
                facility_day=week_number,
            )

    def test_calendar_holiday(self):
        base_datetime = tz.localize(datetime(2015, 8, 5))
        DAY = weekday(base_datetime.isoweekday() - 1)
        Holiday.objects.create(name='holiday', date=base_datetime)
        calendar = Calendar()
        appt_datetime = calendar.best_datetime_not_holiday(base_datetime)
        self.assertNotEqual(base_datetime, appt_datetime)
        new_day = weekday(DAY.weekday + 1)
        self.assertEqual(tz.localize(datetime(2015, 8, 6)), appt_datetime + relativedelta(weekday=new_day(+1)))
        self.assertIn(new_day, calendar.allowed_weekdays)

    def test_calendar_holiday2(self):
        base_datetime = tz.localize(datetime(2015, 8, 5))
        DAY = weekday(base_datetime.isoweekday() - 1)
        Holiday.objects.create(name='holiday', date=base_datetime)
        Holiday.objects.create(name='holiday', date=base_datetime + timedelta(days=1))
        Holiday.objects.create(name='holiday', date=base_datetime + timedelta(days=2))
        calendar = Calendar()
        appt_datetime = calendar.best_datetime_not_holiday(base_datetime)
        self.assertNotEqual(base_datetime, appt_datetime)
        new_day = weekday(DAY.weekday + 1)
        self.assertEqual(tz.localize(datetime(2015, 8, 10)), appt_datetime)
        self.assertIn(new_day, calendar.allowed_weekdays)

    def test_calendar_holiday3(self):
        base_datetime = tz.localize(datetime(2015, 8, 5))
        DAY = weekday(base_datetime.isoweekday() - 1)
        for n in range(6):
            Holiday.objects.create(name='holiday', date=base_datetime + timedelta(days=n))
        calendar = Calendar()
        appt_datetime = calendar.best_datetime_not_holiday(base_datetime)
        self.assertNotEqual(base_datetime, appt_datetime)
        new_day = weekday(DAY.weekday + 1)
        self.assertEqual(tz.localize(datetime(2015, 8, 11)), appt_datetime)
        self.assertIn(new_day, calendar.allowed_weekdays)

    def test_calendar_for_facility_with_holiday(self):
        base_datetime = tz.localize(datetime(2015, 8, 5))
        DAY = weekday(base_datetime.isoweekday() - 1)
        for n in range(7):
            Holiday.objects.create(name='holiday', date=base_datetime + timedelta(days=n))
        facility = Facility.objects.create(name='gumare clinic')
        for n in [1, 3]:
            FacilityDay.objects.create(
                facility=facility,
                facility_day=n,
            )
        calendar = Calendar(facility=facility)
        appt_datetime = calendar.best_datetime_not_holiday(base_datetime)
        self.assertNotEqual(base_datetime, appt_datetime)
        self.assertEqual(tz.localize(datetime(2015, 8, 13)), appt_datetime)
        new_day = weekday(DAY.weekday + 1)
        self.assertIn(new_day, calendar.allowed_weekdays)

    def test_not_busy(self):
        facility = Facility.objects.create(name='gumare clinic')
        for n in [1, 3]:
            FacilityDay.objects.create(
                facility=facility,
                facility_day=n,
                appointments_per_day=10,
            )
        appt_datetime = tz.localize(datetime(2015, 8, 4))
        for n in range(11):
            Appointment.objects.create(
                subject='subject{}'.format(n),
                appt_datetime=appt_datetime,
                facility=facility)
        self.assertEqual(Appointment.objects.filter(facility=facility).count(), 11)
        calendar = Calendar(facility=facility, appointment_model=Appointment)
        appt_datetime = calendar.best_datetime_not_busy(appt_datetime)
        self.assertEqual(tz.localize(datetime(2015, 8, 6)), appt_datetime)

    def test_calendar_busy(self):
        base_datetime = tz.localize(datetime(2015, 8, 5))
        facility = Facility.objects.create(name='gumare clinic')
        for n in [0, 1, 2, 3, 4]:
            FacilityDay.objects.create(
                facility=facility,
                facility_day=n,
                appointments_per_day=10,
            )
        for n in range(11):
            Appointment.objects.create(
                subject='subject{}'.format(n),
                appt_datetime=base_datetime,
                facility=facility)
        self.assertEqual(Appointment.objects.filter(facility=facility).count(), 11)
        calendar = Calendar(facility=facility, appointment_model=Appointment)
        appt_datetime = calendar.best_datetime(base_datetime, base_datetime.isoweekday() - 1)
        self.assertEqual(tz.localize(datetime(2015, 8, 6)), appt_datetime)
