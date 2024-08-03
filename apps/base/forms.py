from django import forms
from django.db.models import TextChoices


class PaginatedByForm(forms.Form):
    
    class PaginationChoices(TextChoices):
        TEN = '10', '10'
        TWENTY_FIVE = '25', '25'
        FIFTY = '50', '50'
        ALL = 'all', 'All'
    
    per_page = forms.ChoiceField(
        choices=PaginationChoices.choices,
        required=False,
        initial=PaginationChoices.TEN,
        label=''
    )
    
    def __init__(self, attrs: dict, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
            
        self.fields['per_page'].widget.attrs['class'] = (
            'px-2 py-1 rounded-lg bg-slate-50 outline-none focus:ring-2 focus:ring-orange-500 border-none hover:bg-slate-100 duration-150'
        )
        self.fields['per_page'].widget.attrs['hx-include'] = '[data-include]'
        self.fields['per_page'].widget.attrs['hx-swap']= 'outerHTML'
        self.fields['per_page'].widget.attrs['data-include']= ''
        
        for k, v in attrs.items():
            self.fields['per_page'].widget.attrs[k] = v