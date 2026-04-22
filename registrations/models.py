from django.db import models
from events.models import Event, Department
import uuid


class Registration(models.Model):
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('5th Year', '5th Year'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='registrations')
    year_level = models.CharField(max_length=20, choices=YEAR_CHOICES)
    section = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    registration_code = models.CharField(max_length=36, default=uuid.uuid4, unique=True, editable=False)
    is_attended = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('event', 'full_name', 'department', 'year_level', 'section')

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"


class Attendance(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='attendance')
    checked_in_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f"{self.registration.full_name} checked in at {self.checked_in_at}"
