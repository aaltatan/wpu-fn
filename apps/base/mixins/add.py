from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render

from .utils import RaiseAddExceptions

class AddMixin(RaiseAddExceptions):
    
    # get
    form_class = None
    template_name = None
    # post
    base_template_name = None
    add_form_template = None
    success_path = None

    def get(self, request: HttpRequest) -> HttpResponse:
        
        self.raise_exceptions_if_necessary()
        
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest) -> HttpResponse:
        
        context = {'form': self.form_class()}
        return render(request, self.add_form_template, context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        
        form = self.form_class(request.POST)
        context = {'form': form}
        
        if form.is_valid():
            
            form.save()
            messages.info(request, _('done'), 'bg-green-600')
            
            if request.POST.get('save'):
                response = render(request, self.base_template_name)
                response['Hx-Retarget'] = '#app'
                response['Hx-Reselect'] = '#app'
                response['Hx-Reswap'] = 'outerHTML'
                response['Hx-Push-Url'] = reverse(self.success_path)
                return response
            
            if request.POST.get('save_and_add_another'):
                context = {'form': self.form_class()}
            
        return render(request, self.add_form_template, context)