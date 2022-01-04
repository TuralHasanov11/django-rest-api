from django.db.models import fields
from auth_user import models
from rest_framework import serializers
from blog.models import BlogPost
import sys
import os
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage

IMAGE_SIZE_MAX_BYTES = 1024*1024*2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

class BlogPostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('getUsername')
    image = serializers.SerializerMethodField('validateImageUrl')
    class Meta:
        model = BlogPost
        fields = ['id','title', 'body', 'image', 'slug', 'username', 'created_at', 'updated_at']

    def getUsername(self, post):
        return post.author.username

    def validateImageUrl(self, post):
        image = post.image
        newUrl = image.url

        if '?' in newUrl:
            newUrl = image.url[:image.url.rfind('?')]

        return newUrl

class BlogPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']
    
    def validate(self, post):
        try:
            title = post['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError({'message':'Title to be longer than {MIN_TITLE_LENGTH}'})
            body = post['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError({'message':'Body to be longer than {MIN_BODY_LENGTH}'})
            image = post['image']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(Location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
                os.remove(url)
                raise serializers.ValidationError({'message':'Image to be smaller than 2MB'})

            img = cv2.imread(url)
            dimensions = img.shape

            aspectRatio = dimensions[1] / dimensions[0] # 0 - Width, 1 - Height, 
            if aspectRatio < 1:
                os.remove(url)
                raise serializers.ValidationError({'message':'Image height to be smaller than width'})
        
            os.remove(url)
        except KeyError:
            pass

        return post


class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'author']
    
    def save(self, post):
        try:
            title = post['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError({'message':'Title to be longer than {MIN_TITLE_LENGTH}'})
            body = post['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError({'message':'Body to be longer than {MIN_BODY_LENGTH}'})
            image = post['image']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(Location=url)

            post = BlogPost(
                author=self.validated_data['author'],
                title = title,
                body = body,
                image=image
            )

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
                os.remove(url)
                raise serializers.ValidationError({'message':'Image to be smaller than 2MB'})

            img = cv2.imread(url)
            dimensions = img.shape

            aspectRatio = dimensions[1] / dimensions[0] # 0 - Width, 1 - Height, 
            if aspectRatio < 1:
                os.remove(url)
                raise serializers.ValidationError({'message':'Image height to be smaller than width'})
        
            os.remove(url)
            post.save()
            return post
        except KeyError:
            raise serializers.ValidationError({'message':'Fields are required'})

        return post