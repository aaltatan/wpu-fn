from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


SCRIPT = """
    let targetId = $event.target.getAttribute('id');
    let criteria = selectedRows.filter(el => el === targetId).length;
    if (criteria) {
        selectedRows = selectedRows.filter(el => el !== targetId);
    } else {
        selectedRows.push(targetId);
    }
"""

class SelectFacultyForm(forms.ModelForm):
    
    selected = forms.BooleanField(
        required=False, 
        initial=False, 
        label='',
        widget=forms.CheckboxInput(
            attrs={
                'x-on:change': SCRIPT,
                'class': 'accent-orange-500',
                'data-check': '',
            }
        )
    )
    
    class Meta:
        model = models.Faculty
        fields = []

class FacultyForm(forms.ModelForm):
    
    class Meta:
        model = models.Faculty
        fields = ['name']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('faculty name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            })
        }
