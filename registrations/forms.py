from django import forms
from .models import Registration
from events.models import Department


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['full_name', 'email', 'department', 'year_level', 'section', 'contact_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition',
                'placeholder': 'e.g. Juan Dela Cruz',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition',
                'placeholder': 'e.g. juan@email.com (optional)',
            }),
            'department': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition',
            }),
            'year_level': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition',
            }),
            'section': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition',
                'placeholder': 'e.g. A, B, C',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition',
                'placeholder': 'e.g. 09123456789 (optional)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['contact_number'].required = False
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].empty_label = "Select your department"
        self.fields['year_level'].widget.choices = [('', 'Select year level')] + list(self.fields['year_level'].widget.choices)[1:]
