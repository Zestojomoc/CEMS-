from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.index, name='index'),

    # Events CRUD
    path('events/', views.manage_events, name='manage_events'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Registrations
    path('registrations/', views.registrations_list, name='registrations'),
    path('registrations/<int:pk>/delete/', views.registration_delete, name='registration_delete'),
    path('registrations/export/', views.export_csv, name='export_csv'),

    # Attendance
    path('attendance/', views.attendance_page, name='attendance'),
    path('attendance/check-in/', views.check_in, name='check_in'),
    path('attendance/toggle/<int:pk>/', views.toggle_attendance, name='toggle_attendance'),

    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    path('analytics/data/', views.analytics_data, name='analytics_data'),

    # Announcements
    path('announcements/', views.announcements, name='announcements'),
]
