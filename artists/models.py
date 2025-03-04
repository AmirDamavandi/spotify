from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
# Create your models here.


class Artist(User):

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')