from django.views.generic import ListView, View
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from . import models, forms, filters
from .mixins import CannotDeleteFacultyMixin

from apps.base import forms as base_forms

from apps.base.mixins.list import ListMixin
from apps.base.mixins.create import CreateMixin
from apps.base.mixins.update import UpdateMixin
from apps.base.mixins.delete import DeleteMixin
from apps.base.mixins.bulk import BulkActionsMixin


class ListTableView(ListMixin, ListView):
    
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


class BulkActionsView(BulkActionsMixin, View):
    
    model = models.Faculty


class CreateView(CreateMixin, View):
    
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/create.html'
    form_template_name = 'partials/create-form.html'


class UpdateView(UpdateMixin, View):
    
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/update.html'
    form_template_name = 'partials/update-form.html'


class DeleteView(DeleteMixin, CannotDeleteFacultyMixin, View):
    
    model = models.Faculty
    modal_template_name = 'partials/delete-modal.html'
