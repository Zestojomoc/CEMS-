from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError
from events.models import Event
from .models import Registration
from .forms import RegistrationForm


def register(request, event_id):
    event = get_object_or_404(Event, pk=event_id, is_active=True)

    if not event.is_registration_open:
        messages.error(request, 'Registration for this event is closed.')
        return redirect('events:event_detail', pk=event.pk)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                registration = form.save(commit=False)
                registration.event = event
                registration.save()

                return redirect('registrations:success', registration_code=registration.registration_code)

            except IntegrityError:
                messages.error(
                    request,
                    'You have already registered for this event with the same name, department, year, and section.'
                )
    else:
        form = RegistrationForm()

    return render(request, 'registrations/register.html', {
        'form': form,
        'event': event,
    })


def success(request, registration_code):
    registration = get_object_or_404(Registration, registration_code=registration_code)
    return render(request, 'registrations/success.html', {
        'registration': registration,
    })
