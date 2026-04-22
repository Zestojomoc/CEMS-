from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('<int:event_id>/', views.register, name='register'),
    path('success/<str:registration_code>/', views.success, name='success'),
]
