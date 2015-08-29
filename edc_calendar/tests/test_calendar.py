import unittest

from datetime import datetime
from dateutil.relativedelta import relativedelta, SU, MO, TU, WE, TH, FR, SA

from edc_calendar.calendar import Calendar


class TestCalendar(unittest.TestCase):

    def test_counter(self):
        fn = Calendar().day_counter
        expected_answers = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4]
        for i in range(12):
            self.assertEqual(expected_answers[i], fn(i))

    def test_allowed_weekday(self):
        calendar = Calendar()
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
        calendar = Calendar(allowed_weekdays=[TU, TH], forward_only=False)
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
        calendar = Calendar(allowed_weekdays=[TU, WE, TH], forward_only=False)
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
        self.assertEqual(TU, calendar.best_day(day))
        day = SA
        self.assertEqual(TU, calendar.best_day(day))
        day = SU
        self.assertEqual(TU, calendar.best_day(day))

    def test_allowed_weekday_limited4(self):
        calendar = Calendar(allowed_weekdays=[MO, WE, FR], forward_only=False)
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
        my_datetime = datetime(2015, 8, 5)
        new_appt_datetime = my_datetime + relativedelta(months=3)
        calendar = Calendar()  # forward_only=True
        best_datetime = calendar.best_datetime(new_appt_datetime, my_datetime.isoweekday() - 1)
        self.assertEqual(best_datetime, datetime(2015, 11, 11, 0, 0))
        self.assertEqual(my_datetime.isoweekday(), best_datetime.isoweekday())

    def test_calc_best_appt_date_lands_on_best_day(self):
        """Asserts finds best datetime on previous wednesday after new_appt_datetime."""
        my_datetime = datetime(2015, 8, 5)
        new_appt_datetime = my_datetime + relativedelta(months=3)
        calendar = Calendar(forward_only=False)
        best_datetime = calendar.best_datetime(new_appt_datetime, my_datetime.isoweekday() - 1)
        self.assertEqual(best_datetime, datetime(2015, 11, 4, 0, 0))
        self.assertEqual(my_datetime.isoweekday(), best_datetime.isoweekday())

if __name__ == '__main__':
    unittest.main()
