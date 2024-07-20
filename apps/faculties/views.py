from . import models, forms, filters
from ..base.mixins.delete_modal import DeleteModalMixin
from ..base.mixins.add_new import AddNewMixin
from ..base.mixins.index_filter_pagination import (
    IndexFilterPaginationMixin
)

from django.views.generic import ListView, View
from django.utils.translation import gettext_lazy as _


class FacultyList(IndexFilterPaginationMixin, ListView):
    
    model = models.Faculty
    filter_class = filters.FacultyFilterSet
    template_name = 'apps/faculties/partials/table.html'
    index_template_name = 'apps/faculties/index.html'
    paginate_by = 20


class AddView(AddNewMixin, View):
    
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/add.html'
    base_template_name = 'apps/faculties/index.html'
    add_form_template = 'apps/faculties/partials/add-form.html'
    success_path = 'faculties:index'


class DeleteView(DeleteModalMixin, View):
    
    model = models.Faculty
    class_name = _('faculty')
    template_name = 'apps/faculties/partials/delete-modal.html'
    hx_location_path = 'faculties:index'
    hx_location_target = '#faculties-table'