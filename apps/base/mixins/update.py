from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from . import utils


class UpdateMixin(utils.HelperMixin):
    
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        
        instance = get_object_or_404(self.get_model_class(), slug=slug)
        
        if self.template_name is None:
            raise Exception('you need to set template_name')
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest, slug: int) -> HttpResponse:
        
        instance = get_object_or_404(self.get_model_class(), slug=slug)
        
        if self.form_template_name is None:
            raise Exception('you need to set form_template_name')
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        return render(request, self.form_template_name, context)
    
    def post(self, request: HttpRequest, slug: int) -> HttpResponse:
            
        instance = get_object_or_404(self.get_model_class(), slug=slug)
        
        form = self.form_class(data=request.POST, instance=instance)
        context = {'form': form, 'instance': instance}
        
        if form.is_valid():
            
            form.save()
            messages.info(request, _('done'), 'bg-green-600')
            
            if request.POST.get('update'):
                response = render(request, self.get_index_template_name())
                response['Hx-Retarget'] = '#app'
                response['Hx-Reselect'] = '#app'
                response['Hx-Reswap'] = 'outerHTML'
                response['Hx-Push-Url'] = reverse(self.get_success_path())
                return response
            
        return render(request, self.form_template_name, context)