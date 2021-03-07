from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)

from ..admin_site import edc_calender_admin
from ..forms import EventForm
from ..models import Event


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'



@admin.register(Event, site=edc_calender_admin)
class EventAdmin(
        ModelAdminMixin, admin.ModelAdmin):

    form = EventForm

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'start_time',
                'end_time',
            )}),
        audit_fieldset_tuple)

    search_fields = ['title']
