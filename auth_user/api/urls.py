from django.urls import path
from .views import (
    register, profile, profileUpdate, ObtainAuthTokenView
)
from rest_framework.authtoken.views import obtain_auth_token


app_name='auth_user'

urlpatterns = [
    path('register', register, name='register'), 
    path('login', ObtainAuthTokenView.as_view(), name='login'),
    path('profile', profile, name='profile'), 
    path('profile/update', profileUpdate, name='profile_update'), 
]
