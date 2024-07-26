from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render

from ..exceptions import (
    FormClassNotFound,
    TemplateNameNotFound,
    BaseTemplateNameNotFound,
    AddFormTemplateNameNotFound,
    SuccessPathNotFound,
)

class AddMixin:
    
    form_class = None
    template_name = None
    base_template_name = None
    add_form_template = None
    success_path = None

    def get(self, request: HttpRequest) -> HttpResponse:
        
        if self.form_class is None:
            raise FormClassNotFound(
                'you need to set form_class like `forms.FacultyForm`'
            )
        
        if self.template_name is None:
            raise TemplateNameNotFound(
                'you need to set template_name like `apps/faculties/add.html`'
            )
        
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest) -> HttpResponse:
        
        context = {'form': self.form_class()}
        return render(request, self.add_form_template, context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        
        if self.base_template_name is None:
            raise BaseTemplateNameNotFound(
                'you need to set base_template_name like `apps/faculties/index.html`'
            )
        
        if self.add_form_template is None:
            raise AddFormTemplateNameNotFound(
                'you need to set add_form_template like `apps/faculties/partials/add-form.html`'
            )
        
        if self.success_path is None:
            raise SuccessPathNotFound(
                'you need to set success_path like `faculties:index`'
            )
        
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