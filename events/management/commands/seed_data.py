from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Department, Event
from dashboard.models import Announcement


class Command(BaseCommand):
    help = 'Seeds the database with sample data for CEMS'

    def handle(self, *args, **options):
        self.stdout.write('Seeding departments...')
        departments_data = [
            ('College of Engineering', 'COENG'),
            ('College of Education', 'COE'),
            ('College of Science', 'COS'),
            ('College of Industrial Technology', 'CIT'),
        ]
        for name, code in departments_data:
            Department.objects.get_or_create(name=name, code=code)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(departments_data)} departments'))

        self.stdout.write('Seeding events...')
        now = timezone.now()
        events_data = [
            {
                'title': 'Tech Innovators Summit 2026',
                'description': 'A full-day summit featuring industry speakers, tech demos, and networking opportunities. Students from all departments are welcome to attend and explore the latest trends in technology, AI, and software development.\n\nHighlights:\n• Keynote by industry professionals\n• Hands-on workshops\n• Project showcases\n• Networking lunch',
                'date': (now + timedelta(days=14)).date(),
                'time': '09:00:00',
                'location': 'Main Auditorium',
                'registration_deadline': now + timedelta(days=12),
                'participant_limit': 200,
                'status': 'upcoming',
            },
            {
                'title': 'Sportsfest 2026',
                'description': 'Annual inter-departmental sports competition featuring basketball, volleyball, badminton, and more. Show your department pride and compete for the championship!\n\nEvents include:\n• Basketball (Men/Women)\n• Volleyball\n• Badminton\n• Table Tennis\n• Chess',
                'date': (now + timedelta(days=21)).date(),
                'time': '07:00:00',
                'location': 'College Gymnasium',
                'registration_deadline': now + timedelta(days=18),
                'participant_limit': 500,
                'status': 'upcoming',
            },
            {
                'title': 'Career Fair & Job Expo',
                'description': 'Meet recruiters from top companies and explore career opportunities. Bring your resume and dress professionally. Open to all year levels.\n\nParticipating companies include major tech firms, engineering companies, and business organizations.',
                'date': (now + timedelta(days=7)).date(),
                'time': '10:00:00',
                'location': 'Function Hall',
                'registration_deadline': now + timedelta(days=5),
                'participant_limit': 300,
                'status': 'upcoming',
            },
            {
                'title': 'Cultural Night: Fiesta del Arte',
                'description': 'An evening of cultural performances, art exhibitions, and food. Celebrate the rich diversity of our college community through dance, music, theater, and visual arts.',
                'date': (now + timedelta(days=30)).date(),
                'time': '18:00:00',
                'location': 'Open Air Theater',
                'registration_deadline': now + timedelta(days=28),
                'participant_limit': 0,
                'status': 'upcoming',
            },
            {
                'title': 'Hackathon: Code for Change',
                'description': 'A 24-hour coding competition where teams build solutions for social good. Open to all CCS students. Prizes worth PHP 50,000 up for grabs!\n\nTheme: Sustainable Development Goals',
                'date': (now + timedelta(days=10)).date(),
                'time': '08:00:00',
                'location': 'CCS Computer Lab',
                'registration_deadline': now + timedelta(days=8),
                'participant_limit': 100,
                'status': 'upcoming',
            },
            {
                'title': 'Leadership Workshop Series',
                'description': 'A 3-day workshop series on leadership, communication, and project management. Perfect for student leaders and aspiring managers.',
                'date': (now - timedelta(days=2)).date(),
                'time': '13:00:00',
                'location': 'Conference Room B',
                'registration_deadline': now - timedelta(days=5),
                'participant_limit': 50,
                'status': 'ongoing',
            },
        ]

        for data in events_data:
            Event.objects.get_or_create(title=data['title'], defaults=data)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(events_data)} events'))

        self.stdout.write('Seeding announcements...')
        announcements_data = [
            {
                'title': '🎓 Registration is now open!',
                'content': 'Event registration for the upcoming academic activities is now open. Visit the Events page to browse and register.',
            },
            {
                'title': '📢 Reminder: Career Fair on campus',
                'content': 'Don\'t forget to register for the Career Fair & Job Expo. Bring your updated resume and dress professionally.',
            },
        ]
        for data in announcements_data:
            Announcement.objects.get_or_create(title=data['title'], defaults=data)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(announcements_data)} announcements'))

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@cems.local',
                password='admin123',
                first_name='CEMS',
                last_name='Administrator',
            )
            self.stdout.write(self.style.SUCCESS('  Created admin user (admin / admin123)'))
        else:
            self.stdout.write('  Admin user already exists')

        self.stdout.write(self.style.SUCCESS('\n✓ Seed data loaded successfully!'))
