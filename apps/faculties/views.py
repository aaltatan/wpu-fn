from django.views.generic import ListView, View
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models, forms, filters
from apps.base import forms as base_forms

from .mixins import CannotDeleteFacultyMixin
from apps.base.mixins.list import ListMixin
from apps.base.mixins.create import CreateMixin
from apps.base.mixins.update import UpdateMixin
from apps.base.mixins.delete import DeleteMixin
from apps.base.mixins.bulk import BulkActionsMixin


class ListTableView(LoginRequiredMixin, 
                    PermissionRequiredMixin, 
                    ListMixin, 
                    ListView):
    
    permission_required = 'faculties.view_faculty'
    
    model = models.Faculty
    filter_class = filters.FacultyFilterSet
    select_filter_class = forms.SelectFacultyForm
    
    template_name = 'apps/faculties/partials/table.html'
    index_template_name = 'apps/faculties/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('faculties:index'),
        'hx-target': '#faculties-table',
    }


class BulkActionsView(LoginRequiredMixin, 
                      PermissionRequiredMixin, 
                      BulkActionsMixin, 
                      View):
    
    permission_required = [
        'faculties.delete_faculty'
    ]
    model = models.Faculty


class CreateView(LoginRequiredMixin, 
                 PermissionRequiredMixin, 
                 CreateMixin, 
                 View):
    
    permission_required = 'faculties.add_faculty'
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/create.html'
    form_template_name = 'partials/create-form.html'


class UpdateView(LoginRequiredMixin, 
                 PermissionRequiredMixin, 
                 UpdateMixin, 
                 View):
    
    permission_required = 'faculties.update_faculty'
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/update.html'
    form_template_name = 'partials/update-form.html'


class DeleteView(LoginRequiredMixin, 
                 PermissionRequiredMixin, 
                 DeleteMixin, 
                 CannotDeleteFacultyMixin, 
                 View):


    permission_required = 'faculties.delete_faculty'
    model = models.Faculty
    modal_template_name = 'partials/delete-modal.html'
