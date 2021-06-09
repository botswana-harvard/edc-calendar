import calendar
import dateutil.parser as parser

from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from edc_calendar.utils import Calendar
from edc_calendar.models import Event

from ..forms import DateSearchForm


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin, generic.ListView, FormView):

    form_class = DateSearchForm
    model = Event
    template_name = 'edc_calendar/home.html'
    navbar_name = 'edc_calendar'
    navbar_selected_item = 'edc_calendar'

    def form_valid(self, form):
        if form.is_valid():
            d = form.data['month']
            filter_date = (parser.parse(d)).date()
            cal = Calendar(filter_date.year, filter_date.month)
            html_cal = cal.formatmonth(withyear=True)
            html_cal += '</table>'
            context = self.get_context_data(**self.kwargs)
            context.update(
                calendar=mark_safe(html_cal),
                prev_month=prev_month(filter_date),
                next_month=next_month(filter_date))
            return HttpResponseRedirect(
                        reverse('edc_calendar:home_url') +
                        f"?filter_date={filter_date}")

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        filter_date = get_date(self.request.GET.get('filter_date', None))
        cal = Calendar(filter_date.year, filter_date.month)
        html_cal = cal.formatmonth(withyear=True)
        html_cal += '</table>'
        context.update(
            calendar=mark_safe(html_cal),
            prev_month=prev_month(filter_date),
            next_month=next_month(filter_date))
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def get_date(req_month):
    if req_month:
        year, month, _ = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):

    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get('filter_date'):
            qs = qs.filter(appt_datetime__date=self.request.GET.get('filter_date'))
        return qs
