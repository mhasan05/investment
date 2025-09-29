from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from accounts.manager import UserManager #import from account apps
from django.conf import settings
from decimal import Decimal



class UserAuth(AbstractBaseUser,PermissionsMixin):
    class Meta:
        verbose_name_plural = "User"
    username = models.CharField(max_length=10,unique=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=100,unique=True)
    super_agent = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.username
    

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    main_balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    invested_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    lock_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    interest_amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return str(self.user)