from django.urls import path

from .views import (
    ListTableView, 
    AddView, 
    UpdateView,
    DeleteView, 
    BulkDeleteView
)


app_name = 'faculties'

urlpatterns = [
    path('', ListTableView.as_view(), name='index'),
    path('add/', AddView.as_view(), name='add'),
    path('update/<str:slug>/', UpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', DeleteView.as_view(), name='delete'),
    path('bulk-delete/', BulkDeleteView.as_view(), name='bulk-delete'),
]