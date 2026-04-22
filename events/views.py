from django.shortcuts import render, get_object_or_404
from .models import Event, Department
from dashboard.models import Announcement


def home(request):
    upcoming_events = Event.objects.filter(is_active=True).exclude(status='closed')[:6]
    announcements = Announcement.objects.filter(is_active=True)[:3]
    return render(request, 'events/home.html', {
        'events': upcoming_events,
        'announcements': announcements,
    })


def event_list(request):
    events = Event.objects.filter(is_active=True)
    status_filter = request.GET.get('status', '')
    if status_filter:
        events = events.filter(status=status_filter)
    return render(request, 'events/event_list.html', {
        'events': events,
        'status_filter': status_filter,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    return render(request, 'events/event_detail.html', {'event': event})
