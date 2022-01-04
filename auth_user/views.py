from django.contrib import auth
from django.db.models.signals import post_delete
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from blog.models import BlogPost

def register(request):
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'auth_user/register.html', context)


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
        context['login_form'] = form
    else:
        form = LoginForm()
        context['login_form'] = form
        
    return render(request, 'auth_user/login.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context={}
   

    if request.POST:
        form = ProfileUpdateForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileUpdateForm(initial={
            "email":request.user.email,
            "username":request.user.username
        })

    context['profile_form'] = form

    posts = BlogPost.objects.filter(author=request.user)
    context['posts']=posts

    return render(request, 'auth_user/profile.html', context)


def mustAuth(request):
    return render(request, 'auth_user/must_authenticate.html')


def isAuth(func):
    def wrapper(request, **kwargs):
        if request.user.is_authenticated:
            return func(request, **kwargs)
        else:
            return redirect('must_auth')
    return wrapper
