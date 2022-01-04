from django.urls import path, include
from .views import (create, detail, edit)

app_name='blog'

urlpatterns = [
    path('create', create, name='create'),
    path('<slug>', detail, name='detail'),
    path('<slug>/edit', edit, name='edit'),
]
