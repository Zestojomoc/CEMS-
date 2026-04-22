import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from events.models import Event, Department
from registrations.models import Registration, Attendance
from .models import Announcement


@login_required
def index(request):
    import json

    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    active_events = Event.objects.filter(is_active=True).exclude(status='closed').count()
    total_attended = Attendance.objects.count()
    recent_registrations = Registration.objects.select_related('event', 'department')[:10]
    events_with_counts = Event.objects.annotate(reg_count=Count('registrations')).order_by('-date')[:5]

    # Build per-department breakdown for stacked bar chart
    departments = Department.objects.all()
    dept_event_matrix = []
    for dept in departments:
        counts = []
        for event in events_with_counts:
            count = Registration.objects.filter(event=event, department=dept).count()
            counts.append(count)
        dept_event_matrix.append({'label': dept.code, 'data': counts})

    return render(request, 'dashboard/index.html', {
        'total_events': total_events,
        'total_registrations': total_registrations,
        'active_events': active_events,
        'total_attended': total_attended,
        'recent_registrations': recent_registrations,
        'events_with_counts': events_with_counts,
        'dept_event_matrix_json': json.dumps(dept_event_matrix),
    })


# ── Event CRUD ──────────────────────────────────────────────

@login_required
def manage_events(request):
    events = Event.objects.annotate(reg_count=Count('registrations')).order_by('-created_at')
    return render(request, 'dashboard/events.html', {'events': events})


@login_required
def event_create(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        event = Event(
            title=request.POST['title'],
            description=request.POST['description'],
            date=request.POST['date'],
            time=request.POST['time'],
            end_date=request.POST.get('end_date') or None,
            end_time=request.POST.get('end_time') or None,
            location=request.POST['location'],
            registration_deadline=request.POST['registration_deadline'],
            participant_limit=int(request.POST.get('participant_limit', 0) or 0),
            status=request.POST.get('status', 'upcoming'),
            is_active=request.POST.get('is_active') == 'on',
        )
        if 'image' in request.FILES:
            event.image = request.FILES['image']
        event.save()
        messages.success(request, f'Event "{event.title}" created successfully!')
        return redirect('dashboard:manage_events')
    return render(request, 'dashboard/event_form.html', {'departments': departments})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.time = request.POST['time']
        event.end_date = request.POST.get('end_date') or None
        event.end_time = request.POST.get('end_time') or None
        event.location = request.POST['location']
        event.registration_deadline = request.POST['registration_deadline']
        event.participant_limit = int(request.POST.get('participant_limit', 0) or 0)
        event.status = request.POST.get('status', 'upcoming')
        event.is_active = request.POST.get('is_active') == 'on'
        if 'image' in request.FILES:
            event.image = request.FILES['image']
        event.save()
        messages.success(request, f'Event "{event.title}" updated successfully!')
        return redirect('dashboard:manage_events')
    return render(request, 'dashboard/event_form.html', {'event': event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted successfully!')
    return redirect('dashboard:manage_events')


# ── Registrations ───────────────────────────────────────────

@login_required
def registrations_list(request):
    registrations = Registration.objects.select_related('event', 'department').all()

    # Filters
    event_id = request.GET.get('event')
    department_id = request.GET.get('department')
    year = request.GET.get('year')
    section = request.GET.get('section')
    search = request.GET.get('search', '')

    if event_id:
        registrations = registrations.filter(event_id=event_id)
    if department_id:
        registrations = registrations.filter(department_id=department_id)
    if year:
        registrations = registrations.filter(year_level=year)
    if section:
        registrations = registrations.filter(section__icontains=section)
    if search:
        registrations = registrations.filter(
            Q(full_name__icontains=search) | Q(email__icontains=search)
        )

    events = Event.objects.all()
    departments = Department.objects.all()

    return render(request, 'dashboard/registrations.html', {
        'registrations': registrations,
        'events': events,
        'departments': departments,
        'filters': {
            'event': event_id or '',
            'department': department_id or '',
            'year': year or '',
            'section': section or '',
            'search': search,
        }
    })


@login_required
def registration_delete(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    if request.method == 'POST':
        reg.delete()
        messages.success(request, 'Registration deleted.')
    return redirect('dashboard:registrations')


@login_required
def export_csv(request):
    registrations = Registration.objects.select_related('event', 'department').all()

    event_id = request.GET.get('event')
    if event_id:
        registrations = registrations.filter(event_id=event_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Department', 'Year Level', 'Section', 'Contact', 'Event', 'Attended', 'Registered At'])

    def excel_text(value):
        if value in (None, ''):
            return ''
        return f'\t{value}'

    for r in registrations:
        writer.writerow([
            r.full_name, r.email or '', r.department.code, r.year_level,
            r.section, excel_text(r.contact_number), r.event.title,
            'Yes' if r.is_attended else 'No', excel_text(r.registered_at.strftime('%Y-%m-%d %H:%M'))
        ])

    return response


# ── Attendance ──────────────────────────────────────────────

@login_required
def attendance_page(request):
    events = Event.objects.all()
    event_id = request.GET.get('event')
    registrations = None
    selected_event = None

    if event_id:
        selected_event = get_object_or_404(Event, pk=event_id)
        registrations = Registration.objects.filter(event=selected_event).select_related('department')

    return render(request, 'dashboard/attendance.html', {
        'events': events,
        'registrations': registrations,
        'selected_event': selected_event,
    })


@login_required
def check_in(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        # Support both full QR string and plain code
        if code.startswith('CEMS-REG-'):
            code = code.replace('CEMS-REG-', '')

        try:
            registration = Registration.objects.get(registration_code=code)
            if registration.is_attended:
                return JsonResponse({'status': 'already', 'name': registration.full_name})

            registration.is_attended = True
            registration.save()
            Attendance.objects.get_or_create(registration=registration)
            return JsonResponse({'status': 'success', 'name': registration.full_name, 'event': registration.event.title})
        except Registration.DoesNotExist:
            return JsonResponse({'status': 'not_found'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
def toggle_attendance(request, pk):
    if request.method == 'POST':
        reg = get_object_or_404(Registration, pk=pk)
        reg.is_attended = not reg.is_attended
        reg.save()
        if reg.is_attended:
            Attendance.objects.get_or_create(registration=reg)
        else:
            Attendance.objects.filter(registration=reg).delete()
        messages.success(request, f"Attendance updated for {reg.full_name}.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:attendance'))


# ── Analytics ───────────────────────────────────────────────

@login_required
def analytics(request):
    events = Event.objects.annotate(reg_count=Count('registrations')).order_by('-date')
    dept_stats = Department.objects.annotate(reg_count=Count('registrations')).order_by('-reg_count')

    return render(request, 'dashboard/analytics.html', {
        'events': events,
        'dept_stats': dept_stats,
    })


@login_required
def analytics_data(request):
    from registrations.models import Registration

    events = Event.objects.annotate(reg_count=Count('registrations')).order_by('date')
    departments = Department.objects.annotate(reg_count=Count('registrations')).order_by('-reg_count')

    # Build per-event, per-department matrix for stacked bar chart
    event_ids = [e.id for e in events]
    dept_event_matrix = []
    for dept in departments:
        counts = []
        for event in events:
            count = Registration.objects.filter(event=event, department=dept).count()
            counts.append(count)
        dept_event_matrix.append({
            'label': dept.code,
            'data': counts,
        })

    return JsonResponse({
        'event_labels': [e.title[:25] for e in events],
        'event_data': [e.reg_count for e in events],
        'dept_labels': [d.code for d in departments],
        'dept_data': [d.reg_count for d in departments],
        'dept_event_matrix': dept_event_matrix,
    })


# ── Announcements ──────────────────────────────────────────

@login_required
def announcements(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            Announcement.objects.create(
                title=request.POST['title'],
                content=request.POST['content'],
                is_active=request.POST.get('is_active') == 'on',
            )
            messages.success(request, 'Announcement created!')
        elif action == 'delete':
            Announcement.objects.filter(pk=request.POST.get('pk')).delete()
            messages.success(request, 'Announcement deleted!')
        elif action == 'toggle':
            ann = get_object_or_404(Announcement, pk=request.POST.get('pk'))
            ann.is_active = not ann.is_active
            ann.save()
            messages.success(request, f'Announcement {"activated" if ann.is_active else "deactivated"}!')
        return redirect('dashboard:announcements')

    all_announcements = Announcement.objects.all()
    return render(request, 'dashboard/announcements.html', {'announcements': all_announcements})
