from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render

from . import utils

class CreateMixin(utils.HelperMixin):
    
    def get(self, request: HttpRequest) -> HttpResponse:
        
        if self.form_class is None:
            raise Exception('you need to set form_class')
        
        model_class = self.form_class._meta.model
        model_name = model_class._meta.model_name
        
        if not hasattr(model_class, 'get_create_path'):
            raise NotImplementedError(f'you need to implement get_create_path property in {model_name} model')
        
        context = {'form': self.form_class(), 'instance': model_class}
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest) -> HttpResponse:
        
        context = {'form': self.form_class()}
        return render(request, self.form_template_name, context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        
        form = self.form_class(request.POST)
        context = {'form': form}
        
        if form.is_valid():
            form.save()
            messages.info(request, _('done'), 'bg-green-600')
            
            if request.POST.get('save'):
                return self.get_success_save_update_response()
            
            if request.POST.get('save_and_add_another'):
                context = {'form': self.form_class()}
        
        if self.form_template_name is None:
            raise Exception('you need to set form_template_name')
        
        return render(request, self.form_template_name, context)