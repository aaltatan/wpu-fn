import json
import re

from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from . import utils


class BulkActionsMixin(utils.HelperMixin):
    
    def get(self, request: HttpRequest):
        
        selected_ids = [
            int(re.findall(r'\d+', k)[0]) 
            for k in request.GET.keys()
            if k.endswith('selected')
        ]
        
        if self.model is None:
            raise Exception('you need to set a model')
        
        pks = [
            int(request.GET.get(f'form-{pk}-id'))
            for pk in selected_ids
        ]

        qs = self.model.objects.filter(pk__in=pks)
        instances_names = [instance.name for instance in qs]
        instances_names = ", ".join(instances_names)
        
        if request.GET.get('bulk_delete'):
            message = _('are you sure you want to delete {} ?').format(instances_names)
            
        context = {
            'pks': ",".join([str(pk) for pk in pks]),
            'message': message,
        }
        
        response = render(request, 'partials/confirm-modal.html', context)
        response['Hx-Retarget'] = '#modal'
        return response
    
    def post(self, request: HttpRequest):
        
        response = HttpResponse('')
        
        pks = [int(pk) for pk in request.POST.get('pks').split(",")]
        
        if request.POST.get('bulk_delete'):
            self.model.objects.filter(pk__in=pks).delete()
        
        messages.info(request, _('done'), 'bg-green-600')
        
        hx_location = {
            'path': reverse(self.get_hx_location_path()),
            'values': {**request.POST},
            'target': self.get_hx_location_target(),
            'swap': 'outerHTML',
        }
        response['Hx-Location'] = json.dumps(hx_location)
            
        return response