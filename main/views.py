from django.shortcuts import render
from blog.models import BlogPost
from blog.views import getBlogQuerySet
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

BLOG_POSTS_PER_PAGE = 1
# Create your views here.
def home(request):
    
    query = ""
    if request.GET:
        query = request.GET.get('q','')
        
    posts = getBlogQuerySet(query)
    posts = posts.order_by('-updated_at')

    page = request.GET.get('page',1)
    paginator = Paginator(posts, BLOG_POSTS_PER_PAGE) 
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'main/index.html', context={
        'posts':posts,
        'query':str(query)
    })



    
