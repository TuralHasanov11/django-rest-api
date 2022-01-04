from django.urls import path
from .views import (blogPostDetail, 
    blogPostDelete, 
    blogPostUpdate, 
    blogPostCreate,
    BlogPostList
)

app_name='blog'

urlpatterns = [
    path('', BlogPostList.as_view(), name='index'),
    path('create', blogPostCreate, name='create'),
    path('<slug>/', blogPostDetail, name='detail'),
    path('<slug>/update', blogPostUpdate, name='update'),
    path('<slug>/delete', blogPostDelete, name='delete'),
   
]
