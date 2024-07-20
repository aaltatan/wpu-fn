from django.db import models
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.urls import reverse



class FacultyManager(models.Manager):
    
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().annotate(
            search=Concat(F('name'), Value(' '), F('name'))
        )


class Faculty(models.Model):
    
    name = models.CharField(
        verbose_name=_('faculty'),
        unique=True,
        max_length=255,
        help_text=_('faculty name'),
    )
    
    objects = FacultyManager()
    
    class Meta:
        verbose_name_plural = _('faculties')
        ordering = ['name']
    
    @property
    def get_delete_path(self):
        return reverse('faculties:delete', kwargs={'pk': self.pk})
    
    def __str__(self) -> str:
        return self.name



