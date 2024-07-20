from . import models

from django import forms
from django.utils.translation import gettext_lazy as _


class FacultyForm(forms.ModelForm):
    
    class Meta:
        model = models.Faculty
        fields = ['name']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('faculty name').capitalize(),
                'class': 'input w-full',
                'autofocus': 'true'
            })
        }