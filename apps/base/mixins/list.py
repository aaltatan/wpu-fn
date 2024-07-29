from typing import Any

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.forms import modelformset_factory

class ListMixin:
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        if self.index_template_name is None:
            raise Exception('you need to set index_template_name')
        
        for property in ['get_delete_path', 'get_update_path']:
            if not hasattr(self.model, property):
                model_name = self.model._meta.model_name.title()
                raise NotImplementedError(f'you implement get_delete_path property on {model_name} model')
        
        if not request.htmx:
            return render(request, self.index_template_name, {})
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context = super().get_context_data(**kwargs)
        
        if self.filter_class is None:
            raise Exception('you need to set filter_class')
        
        filter_from = self.filter_class(self.request.GET).form
        
        SelectFormset = modelformset_factory(
            self.model,
            self.select_filter_class,
            extra=0,
        )
        
        qs = self.get_paginator_queryset()
        
        formset = SelectFormset(queryset=qs)
        
        pagination_form = self.get_pagination_form()
        
        context.update({
            'filter': filter_from, 
            'formset': formset,
            'pagination_form': pagination_form,
        })
        
        return context
    
    def get_paginator_queryset(self):
        
        qs = self.get_queryset()
        paginate_by = self.get_paginate_by(qs)
        paginator: Paginator = self.get_paginator(qs, paginate_by)
        page = self.get_current_page()
        
        return paginator.get_page(page).object_list
        
    def get_queryset(self):
        qs: QuerySet = (
            self
            .filter_class(self.request.GET or self.request.POST)
            .qs
        )
        return qs
    
    def get_current_page(self) -> int:
        return int(self.request.GET.get('page', 1))
    
    def paginate_queryset(self, queryset, page_size):
        paginator: Paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        
        page = self.get_current_page()
        
        if paginator.num_pages < page:
            page = paginator.num_pages
        
        page = paginator.page(page)
        return paginator, page, page.object_list, page.has_other_pages()
    
    def get_pagination_form(self):
        
        if self.paginate_by_form is None:
            raise Exception('you need to set paginate_by_form and paginate_by_form_attributes')
        
        pagination_form = self.paginate_by_form(
            data=self.request.GET,
            attrs=self.paginate_by_form_attributes
        )
        return pagination_form
    
    def get_paginate_by(self, queryset) -> int | None:
        
        pagination_form = self.get_pagination_form()
        
        per_page = self.paginate_by_form.PaginationChoices.TEN
            
        if pagination_form.data.get('per_page'):
            per_page = pagination_form.data.get('per_page')
        
        if pagination_form.data.get('per_page') == 'all':
            per_page = 1_000_000
        
        return int(per_page)