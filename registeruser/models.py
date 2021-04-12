from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=150,null=True,blank=True)
    address = models.TextField()
    slug = models.SlugField(max_length = 250, null = True, blank = True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('post-detail', kwargs=kwargs)
    
    def save(self, *args, **kwargs):
        value = self.user.id
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    