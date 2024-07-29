import json

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from . import utils


class DeleteMixin(utils.HelperMixin):
    
    def get(self, request, *args, **kwargs):
        
        if self.model is None:
            raise Exception('you need to set a model')
        
        instance = get_object_or_404(self.model, slug=kwargs.get('slug'))
        
        instance_name = getattr(instance, 'name')
        
        message = (
            _('are you sure you want to delete {} ?')
            .format(instance_name)
        )
        
        context = {
            'instance': instance,
            'message': message,
            'delete_path': instance.get_delete_path,
            'page': request.GET.get('page'),
        }
        
        if self.modal_template_name is None:
            raise Exception('you need to set modal_template_name')
        
        return render(request, self.modal_template_name, context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        
        slug=kwargs.get('slug')
        
        instance = get_object_or_404(self.model, slug=slug)
        response = HttpResponse('')
        
        if not hasattr(self, 'cannot_delete'):
            raise NotImplementedError('you need to implement cannot_delete method on your view')
        
        cannot_delete_response = self.cannot_delete(request, *args, **kwargs)
        
        if cannot_delete_response is not None:
            return cannot_delete_response
        
        instance.delete()
        messages.info(request, _('done'), 'bg-green-600')
        
        hx_location = {
            'path': reverse(self.get_hx_location_path()),
            'values': {**request.POST},
            'target': self.get_hx_location_target(),
            'swap': 'outerHTML',
        }
        response['Hx-Location'] = json.dumps(hx_location)
        
        return response