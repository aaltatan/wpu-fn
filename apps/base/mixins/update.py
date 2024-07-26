from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from ..exceptions import (
    FormClassNotFound,
    TemplateNameNotFound,
    BaseTemplateNameNotFound,
    UpdateFormTemplateNameNotFound,
    SuccessPathNotFound,
    ModelNotFound,
)

class UpdateMixin:
    
    model = None
    form_class = None
    template_name = None
    base_template_name = None
    update_form_template = None
    success_path = None

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        
        if self.form_class is None:
            raise FormClassNotFound(
                'you need to set form_class like `forms.FacultyForm`'
            )
        
        if self.template_name is None:
            raise TemplateNameNotFound(
                'you need to set template_name like `apps/faculties/add.html`'
            )
            
        if self.model is None:
            raise ModelNotFound(
                'you need to set model like `models.Faculty`'
            )
            
        instance = get_object_or_404(self.model, slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        return render(request, self.template_name, context)
    
    
    def delete(self, request: HttpRequest, slug: int) -> HttpResponse:
        
        instance = get_object_or_404(self.model, slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        return render(request, self.update_form_template, context)
    
    
    def post(self, request: HttpRequest, slug: int) -> HttpResponse:
        
        if self.base_template_name is None:
            raise BaseTemplateNameNotFound(
                'you need to set base_template_name like `apps/faculties/index.html`'
            )
        
        if self.update_form_template is None:
            raise UpdateFormTemplateNameNotFound(
                'you need to set update_form_template like `apps/faculties/partials/update-form.html`'
            )
        
        if self.success_path is None:
            raise SuccessPathNotFound(
                'you need to set success_path like `faculties:index`'
            )
            
        instance = get_object_or_404(self.model, slug=slug)
        
        form = self.form_class(data=request.POST, instance=instance)
        context = {'form': form}
        
        if form.is_valid():
            
            form.save()
            messages.info(request, _('done'), 'bg-green-600')
            
            if request.POST.get('update'):
                response = render(request, self.base_template_name)
                response['Hx-Retarget'] = '#app'
                response['Hx-Reselect'] = '#app'
                response['Hx-Reswap'] = 'outerHTML'
                response['Hx-Push-Url'] = reverse(self.success_path)
                return response
            
        return render(request, self.update_form_template, context)