# expense_tracker/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),  # Include all endpoints from the expenses app
]
