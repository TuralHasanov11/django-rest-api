from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

def uploadLocation(instance, filename, **kwargs):
    filePath = 'blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id),
        title=str(instance.title),
        filename = filename 
    )

    return filePath

class BlogPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=True)
    body = models.TextField(max_length=5000, null=False, blank=True)
    image = models.ImageField(upload_to=uploadLocation, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=BlogPost)
def submissionDelete(sender, instance, **kwargs):
    instance.image.delete(False)

def preSaveBlogPostReceiver(sender, instance, **kwargs):
    instance.slug = slugify(instance.author.username+'-'+instance.title)

pre_save.connect(preSaveBlogPostReceiver, sender=BlogPost)