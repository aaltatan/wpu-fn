from django.views.generic import ListView, View
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from excel_response import ExcelResponse

from . import models, forms, filters
from apps.base import forms as base_forms

from apps.base.mixins.list import ListMixin
from apps.base.mixins.add import AddMixin
from apps.base.mixins.update import UpdateMixin
from apps.base.mixins.delete import DeleteMixin
from apps.base.mixins.bulk_delete import BulkDeleteMixin


class ListTableView(ListMixin, ListView):
    
    model = models.Faculty
    filter_class = filters.FacultyFilterSet
    select_filter_class = forms.SelectFacultyForm
    
    template_name = 'apps/faculties/partials/table.html'
    index_template_name = 'apps/faculties/index.html'
    
    pagination_form = base_forms.PaginatedByForm
    pagination_form_attributes = {
        'hx-get': reverse_lazy('faculties:index'),
        'hx-target': '#faculties-table',
    }
    
    excel_file_name = _('faculties')
    
    def post(self, request):
        
        file_name = self.excel_file_name or 'data'
        qs = self.get_queryset().values()
        
        return ExcelResponse(qs, file_name, force_csv=True)


class BulkDeleteView(BulkDeleteMixin, View):
    
    model = models.Faculty
    hx_location_path = 'faculties:index'
    hx_location_target = '#faculties-table'


class AddView(AddMixin, View):
    
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/add.html'
    base_template_name = 'apps/faculties/index.html'
    add_form_template = 'apps/faculties/partials/add-form.html'
    success_path = 'faculties:index'


class UpdateView(UpdateMixin, View):
    
    model = models.Faculty
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/update.html'
    base_template_name = 'apps/faculties/index.html'
    update_form_template = 'apps/faculties/partials/update-form.html'
    success_path = 'faculties:index'


class DeleteView(DeleteMixin, View):
    
    model = models.Faculty
    class_name = _('faculty')
    template_name = 'apps/faculties/partials/delete-modal.html'
    hx_location_path = 'faculties:index'
    hx_location_target = '#faculties-table'