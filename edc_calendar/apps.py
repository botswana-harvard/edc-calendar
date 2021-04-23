from datetime import datetime
from dateutil.tz import gettz

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings



class AppConfig(DjangoAppConfig):
    name = 'edc_calendar'
    verbose_name = 'Edc Calender'

    def ready(self):
        from edc_calendar import create_or_update_calender_event_on_post_save

if settings.APP_NAME == 'edc_calendar':
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
    

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = 'BHP010'
        protocol_name = 'EDC Calender'
        protocol_number = '010'
        protocol_title = ''
        study_open_datetime = datetime(
            2020, 9, 16, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2023, 12, 31, 23, 59, 59, tzinfo=gettz('UTC'))