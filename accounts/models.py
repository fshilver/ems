from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    email 을 id 로 사용하기 위한 custom user manager
    """

#     def _create_user(self, email, name, password, **extra_fields):
#         if not email:
#             raise ValueError('The Email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_user(self, email, name, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', False)
#         return self._create_user(email, password, name, **extra_fields)


#     def create_superuser(self, email, name, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(email, name, password, **extra_fields)

    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            name,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]
    objects = CustomUserManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def group_names(self):
        return ','.join([g.name for g in self.groups.all()]) if self.groups.count() else ''
        

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name