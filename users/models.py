import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import CASCADE
from .manager import UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    nickname = models.CharField(max_length=128)
    email = models.EmailField(unique=True, max_length=255)
    genders = (('male', 'Male'), ('female', 'Female'), ('prefer not to say', 'Prefer not to say'))
    gender = models.CharField(max_length=20, choices=genders)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    relation = models.ManyToManyField('self', through='Relation')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'gender']

    objects = UserManager()

    def __str__(self):
        return self.nickname

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'

    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')
        unique_together = (('from_user', 'to_user'),)
