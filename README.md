# edc-calendar

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
Returns the best datetime given an appointment datetime and a weekday number that the appointment should fall on. 

	from datetime import datetime
	from dateutil.relativedelta import MO, WE, FR, SA, SU, relativedelta
	from edc_calendar import Calendar
	
	calendar = Calendar(forward_only=False)
    base_appt_datetime = datetime(2015, 8, 5)  # Wednesday
    appt_datetime = base_appt_datetime + relativedelta(months=3)
    print(appt_datetime)  # 2015-11-05 00:00:00, Thursday
    best_datetime = calendar.best_datetime(appt_datetime, base_appt_datetime.isoweekday() - 1)
    print(best_datetime)  # 2015-11-04 00:00:00, Wednesday

