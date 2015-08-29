from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, weekday


class Calendar(object):

    def __init__(self, forward_only=None, allowed_weekdays=None):
        self.forward_only = True if forward_only is None else forward_only
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

    def best_datetime(self, appt_datetime, weekday_number):
        DAY = self.best_day(weekday(weekday_number))
        day1 = weekday(appt_datetime.isoweekday() - 1)
        day2 = weekday(weekday_number)
        if day1 == day2:
            addend = 0
        elif self.distance_forward(day1, day2) > abs(self.distance_backward(day1, day2)):
            addend = -1 if not self.forward_only else 1
        else:
            addend = 1
        return appt_datetime + relativedelta(weekday=DAY(addend))

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

    def best_datetime_not_busy(self, appt_datetime):
        """Increments appointment date to a day where the maximum appts per day has not been reached."""
        return appt_datetime

    def best_datetime_not_holiday(self, appt_datetime):
        """Increments appointment date forward from a holiday."""
        return appt_datetime
