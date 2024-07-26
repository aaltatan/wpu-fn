import json

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from ..exceptions import (
    InstanceNameNotFound,
    ModelNotFound,
    TemplateNameNotFound,
    HtmxLocationTargetNotFound,
    HtmxLocationPathNotFound
)


class DeleteMixin:
    
    class_name = None
    model = None
    template_name = None
    hx_location_path = None
    hx_location_target = None
    
    def get(self, request, *args, **kwargs):
        
        if self.class_name is None:
            raise InstanceNameNotFound(
                'you must define class_name'
            )
        if self.model is None:
            raise ModelNotFound(
                'you must define a model'
            )
        if self.template_name is None:
            raise TemplateNameNotFound(
                'you must define the template_name'
            )
            
        instance = get_object_or_404(self.model, slug=kwargs.get('slug'))
        
        if not hasattr(instance, 'get_delete_path'):
            raise NotImplementedError('you need to implement get_delete_path property in your model.')
        
        instance_name = getattr(instance, 'name')
        
        message = (
            _('are you sure you want to delete {} {} ?')
            .format(self.class_name, instance_name)
        )
        
        context = {
            'instance': instance,
            'message': message,
            'delete_path': instance.get_delete_path,
            'page': request.GET.get('page'),
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        
        if self.hx_location_path is None:
            raise HtmxLocationPathNotFound(
                'you need to set hx_location_path'
            )
        
        if self.hx_location_target is None:
            raise HtmxLocationTargetNotFound(
                'you need to set hx_location_target'
            )
        
        slug=kwargs.get('slug')
        
        instance = get_object_or_404(self.model, slug=slug)
        response = HttpResponse('')
        
        if False:
            # needs implementation
            messages.info(
                request, 
                _('you can\'t delete this {} ({}) because there is one or more models related to it.').format(self.class_name, instance.name),
                'bg-red-600'
            )
            response['Hx-Retarget'] = '#no-content'
            response['Hx-Reswap'] = 'innerHTML'
            return response
        
        instance.delete()
        messages.info(request, _('done'), 'bg-green-600')
        
        hx_location = {
            'path': reverse(self.hx_location_path),
            'values': {**request.POST},
            'target': self.hx_location_target,
            'swap': 'outerHTML',
        }
        response['Hx-Location'] = json.dumps(hx_location)
        
        return response