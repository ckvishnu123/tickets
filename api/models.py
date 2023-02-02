from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    # first name, last name etc fields will be in AbstractUser
    phone_number = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=500)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    # username field is set as phone number for phone number based login
    # required field is set as empty

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()


class Tickets(models.Model):
    # two options are set for priority field
    ticket_id = models.PositiveIntegerField()
    subject = models.CharField(max_length=1000)
    options = (
        ("urgent", "urgent"),
        ("normal", "normal")
    )
    priority = models.CharField(max_length=200, choices=options, default="normal")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ticket_id
