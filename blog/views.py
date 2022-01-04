from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from .models import BlogPost
from .forms import CreateBlogPostForm, UpdateBlogPostForm
from auth_user.models import AuthUser
from auth_user.views import isAuth
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .policies import canUpdate, canCreate, canDelete

@require_http_methods(["GET", "POST"])
@login_required(login_url='/login', redirect_field_name='')
def create(request):

    if not canCreate(request):
        return redirect('home')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        data = form.save(commit=False)
        author = AuthUser.objects.filter(email=request.user.email).first()
        data.author = author
        data.save()
        form = CreateBlogPostForm()
        messages.success(request, 'Post created successfully!')
        return redirect('blog:create')

    return render(request, 'blog/create.html', context={
        'form':form
    })


def detail(request,slug):
    context = {}

    post = get_object_or_404(BlogPost, slug=slug)

    return render(request, 'blog/detail.html', context={
        'post':post
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='/login', redirect_field_name='')
def edit(request,slug):
    # if not request.user.is_authenticated:
    #     return redirect('must_auth')

    post = get_object_or_404(BlogPost, slug=slug)

    if not canUpdate(request, post):
        return redirect('home')

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=post)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            post = data
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:edit', post.slug)

    form = UpdateBlogPostForm(initial={
        'title':post.title,
        'body':post.body,
        'image':post.image,
    })

    return render(request, 'blog/edit.html', context={
        'form':form
    })


def getBlogQuerySet(query=None):
    queryset = BlogPost.objects
    queries = query.split(" ")
    for q in queries:
        queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q))
    
    queryset = queryset.distinct()

    return queryset


