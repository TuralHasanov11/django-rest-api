from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import fields
from django.contrib.auth import authenticate
from .models import AuthUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Email is required and should be valid email address')

    class Meta:
        model = AuthUser
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = AuthUser
        fields = ('email', 'password')

    def clean(self):

        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login credentials')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields= ('email','username')
    
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            try:
                profile = AuthUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except AuthUser.DoesNotExist:
                return email
            raise forms.ValidationError(f'Email {profile.email} does not exist')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                profile = AuthUser.objects.exclude(pk=self.instance.pk).get(username=username)
            except AuthUser.DoesNotExist:
                return username
            raise forms.ValidationError(f'Username {profile} does not exist')