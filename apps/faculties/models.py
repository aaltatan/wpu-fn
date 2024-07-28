from django.db import models
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


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
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        allow_unicode=True,
    )
    
    objects = FacultyManager()
    
    class Meta:
        verbose_name_plural = _('faculties')
        ordering = ['name']
    
    # @property
    # def get_delete_path(self):
    #     return reverse('faculties:delete', kwargs={'slug': self.slug})
    
    # @property
    # def get_update_path(self):
    #     return reverse('faculties:update', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name



