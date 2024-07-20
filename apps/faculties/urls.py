from django.urls import path
from .views import FacultyList, DeleteView, AddView


app_name = 'faculties'

urlpatterns = [
    path('', FacultyList.as_view(), name='index'),
    path('add/', AddView.as_view(), name='add'),
    path('delete/<int:pk>/', DeleteView.as_view(), name='delete')
]