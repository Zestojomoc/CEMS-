from django.contrib import admin
from .models import Registration, Attendance


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'department', 'year_level', 'section', 'is_attended', 'registered_at')
    list_filter = ('event', 'department', 'year_level', 'is_attended')
    search_fields = ('full_name', 'email')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('registration', 'checked_in_at')
