from django.db import models
from django.contrib.auth.models import  AbstractUser


    

class User(AbstractUser):
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=40, unique=True, blank=False)

    is_admin = models.BooleanField(default=False)
 


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

