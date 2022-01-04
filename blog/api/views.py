from auth_user.api.views import register
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView  
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

from auth_user.models import AuthUser
from blog.models import BlogPost
from .serializers import BlogPostSerializer, BlogPostCreateSerializer, BlogPostUpdateSerializer
from blog.policies import canCreate, canDelete, canUpdate


class BlogPostList(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    search_fields = ['title', 'body', 'author__username']
    filter_backends = [SearchFilter,OrderingFilter]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blogPostDetail(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogPostSerializer(post)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def blogPostUpdate(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)

        if not canUpdate(request, post):
            return Response({'message':'Update forbidden'}, status=status.HTTP_403_FORBIDDEN)

    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogPostUpdateSerializer(post, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(data={'message':'Update success'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def blogPostDelete(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)

        if not canDelete(request, post):
            return Response({'message':'Delete forbidden'}, status=status.HTTP_403_FORBIDDEN)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if post.delete():
        return Response(data={'message':'Delete success'})
    else:
        return Response(data={'message':'Delete failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blogPostCreate(request):
    if not canCreate(request):
            return Response({'message':'Create forbidden'},status=status.HTTP_403_FORBIDDEN)

    data = request.data
    data['author'] = request.user.id

    serializer = BlogPostCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)