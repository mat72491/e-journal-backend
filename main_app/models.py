from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    tags = models.ManyToManyField(Tag, related_name='journal_entries', blank=True)
    
    def __str__(self):
        return self.title
    

