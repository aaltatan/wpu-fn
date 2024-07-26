from typing import Any

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.forms import modelformset_factory

from ..exceptions import (
    IndexTemplateNotFound,
    FilterClassNotFound,
)

class ListMixin:
    
    filter_class = None
    index_template_name = None
    select_filter_class = None
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        if self.index_template_name is None:
            raise IndexTemplateNotFound(
                'you need to set index_template_name like `apps/faculties/index.html`'
            )
            
        if not request.htmx:
            return render(request, self.index_template_name, {})
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        if self.filter_class is None:
            raise FilterClassNotFound('you need to add filter_class like `filters.FacultyFilterSet`')
        
        context = super().get_context_data(**kwargs)
        
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
        pagination_form = self.pagination_form(
            data=self.request.GET,
            attrs=self.pagination_form_attributes
        )
        return pagination_form
    
    def get_paginate_by(self, queryset) -> int | None:
        
        pagination_form = self.get_pagination_form()
        
        per_page = self.pagination_form.PaginationChoices.TEN
            
        if pagination_form.data.get('per_page'):
            per_page = pagination_form.data.get('per_page')
        
        if pagination_form.data.get('per_page') == 'all':
            per_page = 1_000_000
        
        return int(per_page)