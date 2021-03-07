from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, date

from django.utils.safestring import mark_safe

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..utils import Calendar
from ..models import Event


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin, generic.ListView):

    model = Event
    template_name = 'edc_calender/home.html'
    navbar_name = 'edc_calender'
    navbar_selected_item = 'edc_calender'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)

        context.update(calendar=mark_safe(html_cal))
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()