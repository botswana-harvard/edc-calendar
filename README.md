[![Build Status](https://travis-ci.org/botswana-harvard/edc-calendar.svg)](https://travis-ci.org/botswana-harvard/edc-calendar)
[![Coverage Status](https://coveralls.io/repos/botswana-harvard/edc-calendar/badge.svg?branch=develop&service=github)](https://coveralls.io/github/botswana-harvard/edc-calendar?branch=develop)

# edc-calendar


Moved to edc_appointment
See edc_appointment.facility


To schedule an appointment that falls on a day that the clinic is open, isn't a holiday and isn't already over-booked:

    from django.utils import timezone
    from .facility import Facility
    
    suggested_datetime = timezone.now()
    available_datetime = facility.available_datetime(suggested_datetime)


If holidays are entered (in model `Holiday`) and the appointment lands on a holiday, the appointment date is incremented forward to an allowed weekday. Assuming `facility` is configured in `app_config` to only schedule appointments on [TU, TH]:

    from datetime import datetime
    from dateutil.relativedelta import TU, TH
    from django.conf import settings
    from django.utils import timezone

    from .facility import Facility
	from .models import Holiday
    
    Holiday.objects.create(
        name='Id-ul-Adha (Feast of the Sacrifice)',
        date=tz.localize(datetime(2015, 9, 24))
    )
    suggested_datetime = timezone.make_aware(datetime(2015, 9, 24))  # TH
    available_datetime = facility.available_datetime(suggested_datetime)
    print(available_datetime)  # 2015-09-29 00:00:00, TU

You can also set a maximum number of appointments allowed per day. As with the holiday example above, the appointment
date will be incremented forward to an allowed weekday that has not reached the maximum number of appointments.

Configuration
-------------

Add each facility to `app_config.facilities` specifying the facility name, weekdays open and the maximum number of slots available per day:

    from edc_appointment.apps import AppConfig as EdcAppointmentAppConfig

    class AppConfig(EdcAppointmentAppConfig):

        facilities = {
            'clinic1': Facility(name='clinic', days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100])}
            'clinic2': Facility(name='clinic', days=[MO, WE, FR], slots=[30, 30, 30])}
