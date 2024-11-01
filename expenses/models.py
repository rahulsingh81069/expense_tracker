from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    payer = models.ForeignKey(User, related_name='paid_expenses', on_delete=models.CASCADE)
    split_method = models.CharField(max_length=10, choices=(('equal', 'Equal'), ('exact', 'Exact'), ('percentage', 'Percentage')))

class Split(models.Model):
    expense = models.ForeignKey(Expense, related_name='splits', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
