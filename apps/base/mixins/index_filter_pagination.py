from typing import Any

from ..exceptions import (
    IndexTemplateNotFound,
    FilterClassNotFound,
)

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator


class IndexFilterPaginationMixin:
    
    filter_class = None
    index_template_name = None
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        if self.index_template_name is None:
            raise IndexTemplateNotFound(
                'you need to set index_template_name'
            )
            
        if not request.htmx:
            return render(request, self.index_template_name, {})
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        if self.filter_class is None:
            raise FilterClassNotFound('you need to add filter_class')
        
        context = super().get_context_data(**kwargs)
        
        filter_from = self.filter_class(self.request.GET).form
        
        context.update({'filter': filter_from})
        
        return context
        
    def get_queryset(self):
        qs = self.filter_class(self.request.GET).qs
        return qs
    
    def paginate_queryset(self, queryset, page_size):
        paginator: Paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        
        page = int(self.request.GET.get('page', 1))
        
        if paginator.num_pages < page:
            page = paginator.num_pages
        
        page = paginator.page(page)
        return paginator, page, page.object_list, page.has_other_pages()