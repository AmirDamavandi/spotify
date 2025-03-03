from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Artist(User):

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')