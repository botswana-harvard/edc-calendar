[![Build Status](https://travis-ci.org/botswana-harvard/edc-calendar.svg)](https://travis-ci.org/botswana-harvard/edc-calendar)
[![Coverage Status](https://coveralls.io/repos/botswana-harvard/edc-calendar/badge.svg?branch=develop&service=github)](https://coveralls.io/github/botswana-harvard/edc-calendar?branch=develop)

# edc-calendar

To schedule an appointment that falls on a day that the clinic is open, isn't a holiday and isn't already over-booked:

    from datetime import datetime
    from edc_calendar import Calendar
    
    suggested_appt_datetime = datetime(2015, 8, 5)
    appt_datetime = calendar.best_datetime(suggested_appt_datetime)


If holidays are entered (in model `Holiday`) and the appointment lands on a holiday, the appointment date is incremented forward to an allowed weekday:

    import pytz
    from datetime import datetime
    from dateutil.relativedelta import TU, TH
    from django.conf import settings
	from edc_calendar import Calendar, Holiday
    
    tz = pytz.timezone(settings.TIME_ZONE)
    
    Holiday.objects.create(
        name='Id-ul-Adha (Feast of the Sacrifice)',
        date=tz.localize(datetime(2015, 9, 24))
    )
    appt_datetime = datetime(2015, 9, 24)  # TH
    calendar = Calendar(forward_only=False, allowed_weekdays=[TU, TH])
    best_datetime = calendar.best_datetime(appt_datetime, appt_datetime.isoweekday() - 1)
    print(best_datetime)  # 2015-09-29 00:00:00, TU

You can also set a maximum number of appointments allowed per day. As with the holiday example above, the appointment
date will be incremented forward to an allowed weekday that has not reached the maximum number of appointments.

Configuration
-------------

Add facilities (such as clinics) each of which may have different "clinic days":

	facility = Facility.objects.create(name='Gumare Clinic')
	
To each facility add the days on which appointments may be made and the maximum number of appointments allowed per day:

    for weekday_number in [TU.weekday, TH.weekday]:
        FacilityDay.objects.create(
            facility=facility,
            facility_day=weekday_number,
            appointments_per_day=10,
        )

You can inspect the days like this:

	>>> FacilityDay.objects.days(facility)
	[TU, TH]
	
Add your holidays

    Holiday.objects.create(
        name='Id-ul-Adha (Feast of the Sacrifice)',
        date=tz.localize(datetime(2015, 9, 24))
    )

calendar.best_day
-----------------
Returns the closest day from the list of allowed days. For example, if a clinic is only open MO, WE, FR:

	from dateutil.relativedelta import MO, WE, FR, SA, SU
	from edc_calendar import Calendar
	
	calendar = Calendar(allowed_days=[MO, WE, FR], forward_only=False)
	print(calendar.best_day(MO)  # MO
	print(calendar.best_day(TU)  # MO
	print(calendar.best_day(WE)  # WE
	print(calendar.best_day(TH)  # WE
	print(calendar.best_day(FR)  # FR
	print(calendar.best_day(SA)  # FR
	print(calendar.best_day(SU)  # MO
	
calendar.best_datetime
----------------------
Returns the best datetime given an appointment datetime and a weekday number that the appointment should fall on. If you do not specify the weekday number that the appointment should fall on (`weekday_number`) the weekday_number of the `suggested_appt_datetime` will be used.

	from datetime import datetime
	from dateutil.relativedelta import MO, WE, FR, SA, SU, relativedelta
	from edc_calendar import Calendar
	
	calendar = Calendar()
    base_appt_datetime = datetime(2015, 8, 5)  # Wednesday
    suggested_appt_datetime = base_appt_datetime + relativedelta(months=3)
    print(suggested_appt_datetime)  # 2015-11-05 00:00:00, Thursday
    best_datetime = calendar.best_datetime(suggested_appt_datetime, base_appt_datetime.isoweekday() - 1)
    print(best_datetime)  # 2015-11-04 00:00:00, Wednesday

	
