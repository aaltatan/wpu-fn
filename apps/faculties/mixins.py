from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


class CannotDeleteFacultyMixin:
    
    def cannot_delete(self, request, *args, **kwargs):
        
        instance = get_object_or_404(self.model, slug=kwargs.get('slug'))
        
        if 1 == 2:
            response = HttpResponse('')
            messages.info(
                request, 
                _('you can\'t delete this ({}) because there is one or more models related to it.').format(instance.name),
                'bg-red-600'
            )
            response['Hx-Retarget'] = '#no-content'
            response['Hx-Reswap'] = 'innerHTML'
            return response
        
        return None