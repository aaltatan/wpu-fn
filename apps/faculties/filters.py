from typing import Any

from django.utils.translation import gettext_lazy as _
from django.forms import widgets
from django.urls import reverse_lazy
from django.db.models import Q

import django_filters as filters

from . import models


attrs: dict[str, Any] = {
    'placeholder': _('search by the name').capitalize(),
    'type': 'search',
    'autocomplete': 'off',
    'class': 'bg-slate-50 outline-none rounded-lg focus:ring-2 focus:ring-orange-500 duration-150 px-4 py-2',
    'hx-get': reverse_lazy('faculties:index'),
    'hx-target': "#container",
    'hx-select': "#container",
    'hx-trigger': 'input changed delay:500ms, search',
    'hx-swap': "outerHTML",
    'hx-include': "[data-include]",
}

class FacultyFilterSet(filters.FilterSet):
    
    name = filters.CharFilter(
        label='',
        widget=widgets.TextInput(attrs=attrs),
        method='filter_name',
    )
    
    def filter_name(self, queryset, name, value):
        keywords = value.split(' ')
        stmt = Q()
        for keyword in keywords:
            stmt &= Q(search__contains=keyword)
        return queryset.filter(stmt)
    
    class Meta:
        model = models.Faculty
        fields = ['name']