import json
import re

from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse

from .utils import RaiseBulkDeleteExceptions

class BulkDeleteMixin(RaiseBulkDeleteExceptions):
    
    model = None
    hx_location_path = None
    hx_location_target = None
        
    def post(self, request: HttpRequest):
        
        self.raise_exceptions_if_necessary()
        
        response = HttpResponse('')
        
        selected_ids = [
            int(re.findall(r'\d+', k)[0]) 
            for k in request.POST.keys()
            if k.endswith('selected')
        ]
        pks = [
            int(request.POST.get(f'form-{pk}-id')) 
            for pk in selected_ids
        ]
        self.model.objects.filter(pk__in=pks).delete()
        
        messages.info(request, _('done'), 'bg-green-600')
        
        hx_location = {
            'path': reverse(self.hx_location_path),
            'values': {**request.POST},
            'target': self.hx_location_target,
            'swap': 'outerHTML',
        }
        response['Hx-Location'] = json.dumps(hx_location)
            
        return response