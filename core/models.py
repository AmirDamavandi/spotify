from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')