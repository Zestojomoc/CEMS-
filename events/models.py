from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    registration_deadline = models.DateTimeField()
    participant_limit = models.PositiveIntegerField(default=0, help_text="0 = unlimited")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return self.title

    @property
    def is_registration_open(self):
        return (
            self.is_active
            and self.status != 'closed'
            and timezone.now() <= self.registration_deadline
            and (self.participant_limit == 0 or self.registration_count < self.participant_limit)
        )

    @property
    def registration_count(self):
        return self.registrations.count()

    @property
    def spots_left(self):
        if self.participant_limit == 0:
            return None  # unlimited
        return max(0, self.participant_limit - self.registration_count)

    @property
    def status_badge_color(self):
        colors = {
            'upcoming': 'emerald',
            'ongoing': 'blue',
            'closed': 'red',
        }
        return colors.get(self.status, 'gray')
