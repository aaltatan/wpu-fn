from random import randint

from django.db import models
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


four_chars_validator = MinLengthValidator(
    4, _('name of the faculty should not be less than 4 characters.')
)


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
        help_text=_('faculty name must be more than 3 characters'),
        validators=[four_chars_validator]
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
    
    @property
    def get_create_path(self):
        return reverse('faculties:create')
    
    @property
    def get_update_path(self):
        return reverse('faculties:update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_path(self):
        return reverse('faculties:delete', kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return self.name


def slugify_signal(sender, instance, *args, **kwargs):
    
    if instance.slug is None or instance == '':
        
        slug = slugify(instance.name, allow_unicode=True)
        class_ = instance.__class__
        
        qs = class_.objects.filter(slug=slug).exclude(id=instance.id)
        
        if qs.exists():
            slug += '-' + str(randint(300_000, 500_000))
            
        instance.slug = slug


pre_save.connect(slugify_signal, Faculty)