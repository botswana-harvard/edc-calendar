from django.contrib import admin

from .models import Holiday, Facility, FacilityDay


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):

    date_hierarchy = 'date'
    list_display = ('name', 'date', )


class FacilityDayInlineAdmin(admin.TabularInline):

    model = FacilityDay
    list_display = ('facility_day', 'appointments_per_day')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):

    list_display = ('name', )
    inlines = [FacilityDayInlineAdmin]


@admin.register(FacilityDay)
class FacilityDayAdmin(admin.ModelAdmin):

    list_display = ('facility', 'facility_day', 'appointments_per_day')
    list_filter = ('facility', )
    list_editable = ('appointments_per_day', )
    search_fields = ('facility__name', )
