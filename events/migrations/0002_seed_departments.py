from django.db import migrations


DEPARTMENTS = [
    ('College of Education', 'COE'),
    ('College of Engineering', 'COENG'),
    ('College of Science', 'COS'),
    ('College of Industrial Technology', 'CIT'),
]


def add_departments(apps, schema_editor):
    Department = apps.get_model('events', 'Department')
    for name, code in DEPARTMENTS:
        Department.objects.using(schema_editor.connection.alias).get_or_create(
            code=code,
            defaults={'name': name},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_departments, migrations.RunPython.noop),
    ]
