from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE  # Ensure you have this constant defined properly

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.PositiveIntegerField(unique=True)  # Account number must be unique and positive
    phone_number1 = models.CharField(max_length=15, unique=True)  # Using CharField for better compatibility with country codes
    phone_number2 = models.CharField(max_length=15, unique=True)  # Same as above
    email = models.EmailField(unique=True)  # To ensure unique emails
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Account {self.account_no} - {self.user.username}"  # More descriptive representation

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)  # CharField is better for postal codes due to alphanumeric possibilities
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Address for {self.user.username}"
