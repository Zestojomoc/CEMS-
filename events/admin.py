from django.contrib import admin
from .models import Department, Event


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name', 'code')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'is_active', 'registration_count')
    list_filter = ('status', 'is_active', 'date')
    search_fields = ('title',)
