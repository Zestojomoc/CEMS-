from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin-panel/', include('dashboard.urls')),
    path('admin-panel/', include('accounts.urls')),
    path('register/', include('registrations.urls')),
    path('', include('events.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
