from django.urls import path

from .views import (
    ListTableView, 
    CreateView, 
    UpdateView,
    DeleteView, 
    BulkActionsView
)


app_name = 'faculties'

urlpatterns = [
    path('', ListTableView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('bulk/', BulkActionsView.as_view(), name='bulk'),
    path('update/<str:slug>/', UpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', DeleteView.as_view(), name='delete'),
]