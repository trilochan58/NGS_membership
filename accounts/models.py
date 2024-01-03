from django.db import models
from django.contrib.auth.models import AbstractUser

from config.validators import validate_phone

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    ROLE = (("A", "Admin"), ("U", "User"))

    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10, unique=True, validators=[validate_phone])
    role = models.CharField(max_length=1, choices=ROLE)
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    
    username = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
