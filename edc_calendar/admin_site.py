from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_header = 'Calendar'
    site_title = 'Calendar'
    index_title = 'Calendar Administration'
    site_url = '/'
edc_calendar_admin = AdminSite(name='edc_calendar_admin')
