from django.db import models
from django.contrib.auth.models import User
from .utils import create_shortened_url

# Create your models here.
class Shortener(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    times_followed = models.PositiveIntegerField(default=0)
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)
    
    
    class Meta:
        ordering = ["-created"]
    
    def __str__(self):
        return f'{self.long_url} to {self.short_url}'
    
    def save(self, *args, **kwargs):
        # If the short url wasn't specified
        if not self.short_url:
                # We pass the model instance that is being saved
            self.short_url = create_shortened_url(self)
        super().save(*args, **kwargs)

class UserAgent(models.Model):
    browser = models.TextField()
    operating_system = models.CharField(max_length=50, blank=True)
    operating_version_string = models.CharField(max_length=50, blank=True)
    user_ip_address = models.CharField(max_length=50, blank=True)
    count = models.IntegerField(default=0)

    
    
class History(models.Model):
    used_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    used_short_url = models.TextField()
        
    def __str__(self):
        return self.used_short_url
        