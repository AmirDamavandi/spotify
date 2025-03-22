from django.contrib.auth.models import BaseUserManager
from django.db import models

class ActiveUsers(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

class UserManager(BaseUserManager):
    def get_queryset(self):
        return ActiveUsers(self.model, using=self._db).active()

    def create_user(self, nickname, email, gender, date_of_birth, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not nickname:
            raise ValueError('Users must have a nickname')

        user = self.model(nickname=nickname, email=self.normalize_email(email), gender=gender, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, gender, date_of_birth, password):
        if not email:
            raise ValueError('Users must have an email address')

        user =  self.create_user(nickname, email, gender, date_of_birth, password)
        user.is_admin = True
        user.save(using=self._db)
        return user