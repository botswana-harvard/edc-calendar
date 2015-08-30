from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, weekday

from .models import FacilityDay, Holiday
from _datetime import timedelta


class Calendar(object):

    appointment_model = None

    def __init__(self, facility=None, forward_only=None, allowed_weekdays=None,
                 appointments_per_day=None, appointment_model=None):
        self.forward_only = False if forward_only is None else forward_only
        self.facility = facility
        self.default_appointments_per_day = appointments_per_day or 100
        self.appointment_model = appointment_model or self.appointment_model
        if self.facility:
            self.allowed_weekdays = FacilityDay.objects.days(facility.name)
        else:
            self.allowed_weekdays = allowed_weekdays or [MO, TU, WE, TH, FR]
        self.allowed_isoweekdays = [d.weekday for d in self.allowed_weekdays]

    def best_day(self, day):
        new_day = None
        if day.weekday not in self.allowed_isoweekdays:
            new_day = self.find_new_day(day.weekday, lambda x: x + 1)
            if not self.forward_only:
                new_day_back = self.find_new_day(day.weekday, lambda x: x - 1)
                if new_day != new_day_back:
                    if self.distance_backward(day, new_day_back) < self.distance_forward(day, new_day):
                        new_day = new_day_back
        return new_day or day

    def best_datetime(self, appt_datetime, weekday_number=None, forward_only=None):
        weekday_number = weekday_number or appt_datetime.isoweekday() - 1
        forward_only = forward_only or self.forward_only
        DAY = self.best_day(weekday(weekday_number))
        day1 = weekday(appt_datetime.isoweekday() - 1)
        day2 = weekday(weekday_number)
        if day1 == day2:
            addend = 0
        elif self.distance_forward(day1, day2) > abs(self.distance_backward(day1, day2)):
            addend = -1 if not forward_only else 1
        else:
            addend = 1
        best_datetime = appt_datetime + relativedelta(weekday=DAY(addend))
        datetime_not_holiday = self.best_datetime_not_holiday(best_datetime)
        datetime_not_busy = self.best_datetime_not_busy(datetime_not_holiday)
        best_datetime = datetime_not_busy
        while datetime_not_holiday != datetime_not_busy:
            datetime_not_holiday = self.best_datetime_not_holiday(best_datetime)
            datetime_not_busy = self.best_datetime_not_busy(datetime_not_holiday)
            best_datetime = datetime_not_busy
        return best_datetime

    def day_counter(self, d):
        d = abs(d)
        return 0 if d == 0 else (d - 6 if d > 6 else d + 1) - 1

    def distance_forward(self, day1, day2):
        distance = 0
        for index, d in enumerate(range(day1.weekday, day1.weekday + 7)):
            if weekday(self.day_counter(d)) == day2:
                distance = index + 1
                break
        return distance

    def distance_backward(self, day1, day2):
        distance = 0
        for index, d in enumerate(range(day1.weekday + 7, day1.weekday, -1)):
            if weekday(self.day_counter(d)) == day2:
                distance = index
                break
        return distance

    def find_new_day(self, n, fn):
        found = None
        while found is None:
            n = self.day_counter(fn(n))
            new_day = weekday(n)
            if new_day in self.allowed_weekdays:
                found = new_day
        return new_day

    def appointments_per_day(self, appt_datetime):
        return FacilityDay.objects.get(
            facility=self.facility, facility_day=appt_datetime.isoweekday() - 1).appointments_per_day

    def best_datetime_not_busy(self, appt_datetime):
        """Increments appointment date forward until the maximum appts per day has not been reached."""
        try:
            while (self.appointment_model.objects.filter(appt_datetime=appt_datetime).count() >=
                    self.appointments_per_day(appt_datetime)):
                appt_datetime = self.increment_forward(appt_datetime)
        except AttributeError as e:
            if '\'NoneType\' object has no attribute \'objects\'' in str(e):
                pass
            else:
                raise AttributeError(e)
        return appt_datetime

    def best_datetime_not_holiday(self, appt_datetime):
        """Increments appointment date forward from a holiday."""
        while Holiday.objects.filter(date=appt_datetime).exists():
            appt_datetime = self.increment_forward(appt_datetime)
        return appt_datetime

    def increment_forward(self, appt_datetime):
        appt_datetime += timedelta(days=1)
        while appt_datetime.isoweekday() - 1 not in self.allowed_isoweekdays:
            appt_datetime += timedelta(days=1)
        return appt_datetime
