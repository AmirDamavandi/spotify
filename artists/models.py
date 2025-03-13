from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Artist(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)


    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')