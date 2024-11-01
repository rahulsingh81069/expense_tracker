from django.contrib import admin
from .models import Expense, Split, User
# Register your models here.
admin.site.register(User)   
admin.site.register(Expense)
admin.site.register(Split)