import pytz

from dateutil.relativedelta import relativedelta, SU, MO, TU, WE, TH, FR, SA, weekday
from datetime import datetime, date, time, timedelta
from django.utils import timezone

from django.conf import settings
from django.test import TestCase

from edc_example.models import Appointment, RegisteredSubject, SubjectConsent

from .calendar import Calendar
from .models import FacilityDay, Facility, Holiday
from edc_example.factories import SubjectConsentFactory

tz = pytz.timezone(settings.TIME_ZONE)


class TestCalendar(TestCase):

    def setUp(self):
        self.subject_identifier = '111111111'
        self.registered_subject = RegisteredSubject.objects.create(subject_identifier=self.subject_identifier)
        my_date = date(2014, 8, 6)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        my_datetime = datetime.combine(my_date, my_time)
        self.subject_consent = SubjectConsentFactory(
            subject_identifier=self.subject_identifier,
            consent_datetime=my_datetime)

    def test_counter(self):
        fn = Calendar().day_counter
        expected_answers = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4]
        for i in range(12):
            self.assertEqual(expected_answers[i], fn(i))

    def test_allowed_weekday(self):
        calendar = Calendar(forward_only=True)
        day = MO
        self.assertEqual(day, calendar.best_day(day))
        day = TU
        self.assertEqual(day, calendar.best_day(day))
        day = WE
        self.assertEqual(day, calendar.best_day(day))
        day = TH
        self.assertEqual(day, calendar.best_day(day))
        day = FR
        self.assertEqual(day, calendar.best_day(day))
        day = SA
        self.assertEqual(MO, calendar.best_day(day))
        day = SU
        self.assertEqual(MO, calendar.best_day(day))

    def test_allowed_weekday_limited(self):
        calendar = Calendar(allowed_weekdays=[TU, TH])
        day = MO
        self.assertEqual(TU, calendar.best_day(day))
        day = TU
        self.assertEqual(TU, calendar.best_day(day))
        day = WE
        self.assertEqual(TU, calendar.best_day(day))
        day = TH
        self.assertEqual(TH, calendar.best_day(day))
        day = FR
        self.assertEqual(TH, calendar.best_day(day))
        day = SA
        self.assertEqual(TH, calendar.best_day(day))
        day = SU
        self.assertEqual(TU, calendar.best_day(day))

    def test_allowed_weekday_limited2(self):
        calendar = Calendar(allowed_weekdays=[TU, WE, TH])
        day = MO
        self.assertEqual(TU, calendar.best_day(day))
        day = TU
        self.assertEqual(TU, calendar.best_day(day))
        day = WE
        self.assertEqual(WE, calendar.best_day(day))
        day = TH
        self.assertEqual(TH, calendar.best_day(day))
        day = FR
        self.assertEqual(TH, calendar.best_day(day))
        day = SA
        self.assertEqual(TH, calendar.best_day(day))
        day = SU
        self.assertEqual(TU, calendar.best_day(day))

    def test_allowed_weekday_limited3(self):
        calendar = Calendar(allowed_weekdays=[TU, WE, TH], forward_only=True)
        day = MO
        self.assertEqual(TU, calendar.best_day(day))
        day = TU
        self.assertEqual(TU, calendar.best_day(day))
        day = WE
        self.assertEqual(WE, calendar.best_day(day))
        day = TH
        self.assertEqual(TH, calendar.best_day(day))
        day = FR
        self.assertEqual(TU, calendar.best_day(day))
        day = SA
        self.assertEqual(TU, calendar.best_day(day))
        day = SU
        self.assertEqual(TU, calendar.best_day(day))

    def test_allowed_weekday_limited4(self):
        calendar = Calendar(allowed_weekdays=[MO, WE, FR])
        day = MO
        self.assertEqual(MO, calendar.best_day(day))
        day = TU
        self.assertEqual(MO, calendar.best_day(day))
        day = WE
        self.assertEqual(WE, calendar.best_day(day))
        day = TH
        self.assertEqual(WE, calendar.best_day(day))
        day = FR
        self.assertEqual(FR, calendar.best_day(day))
        day = SA
        self.assertEqual(FR, calendar.best_day(day))
        day = SU
        self.assertEqual(MO, calendar.best_day(day))

    def test_calc_best_appt_date_lands_on_best_day_forward(self):
        """Asserts finds best datetime on next wednesday after new_appt_datetime."""

        my_date = date(2015, 8, 5)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        my_datetime = datetime.combine(my_date, my_time)
        new_appt_datetime = my_datetime + relativedelta(months=3)
        calendar = Calendar(forward_only=True)
        best_datetime = calendar.best_datetime(new_appt_datetime, my_datetime.isoweekday() - 1)

        my_date = date(2015, 11, 11)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        result = datetime.combine(my_date, my_time)
        self.assertEqual(best_datetime, result)
        self.assertEqual(my_datetime.isoweekday(), best_datetime.isoweekday())

    def test_calc_best_appt_date_lands_on_best_day(self):
        """Asserts finds best datetime on previous wednesday after new_appt_datetime."""
        my_date = date(2015, 8, 5)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        my_datetime = datetime.combine(my_date, my_time)
        new_appt_datetime = my_datetime + relativedelta(months=3)
        calendar = Calendar()
        best_datetime = calendar.best_datetime(new_appt_datetime, my_datetime.isoweekday() - 1)

        my_date = date(2015, 11, 4)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        result = datetime.combine(my_date, my_time)
        self.assertEqual(best_datetime, result)
        self.assertEqual(my_datetime.isoweekday(), best_datetime.isoweekday())

    def test_increment_forwards(self):
        my_date = date(2015, 8, 6)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        my_datetime = datetime.combine(my_date, my_time)
        calendar = Calendar(allowed_weekdays=[TU, TH])
        appt_datetime = calendar.increment_forward(my_datetime)

        my_date = date(2015, 8, 11)
        my_time = time(12, 0, 0, tzinfo=timezone.get_current_timezone())
        result = datetime.combine(my_date, my_time)
        self.assertEqual(appt_datetime, result)

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
                subject_identifier=self.subject_identifier,
                appt_datetime=appt_datetime,
                facility_name=facility.name)
        self.assertEqual(Appointment.objects.filter(facility_name=facility.name).count(), 11)
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
                subject_identifier=self.subject_identifier,
                appt_datetime=base_datetime,
                facility_name=facility.name)
        self.assertEqual(Appointment.objects.filter(facility_name=facility.name).count(), 11)
        calendar = Calendar(facility=facility, appointment_model=Appointment)
        appt_datetime = calendar.best_datetime(base_datetime, base_datetime.isoweekday() - 1)
        self.assertEqual(tz.localize(datetime(2015, 8, 6)), appt_datetime)
