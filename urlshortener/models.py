from django.db import models
from django.contrib.auth.models import User
from .utils import create_shortened_url

# Create your models here.
class ShortenURL(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    times_followed = models.PositiveIntegerField(default=0)
    original_url = models.URLField()
    shorten_url = models.CharField(max_length=15, unique=True, blank=True)

    
    class Meta:
        ordering = ["-created"]
    
    def __str__(self):
        return f'{self.original_url} to {self.shorten_url}'
    
    def save(self, *args, **kwargs):
        # If the short url wasn't specified
        if not self.shorten_url:
                # We pass the model instance that is being saved
            self.shorten_url = create_shortened_url(self)
        super().save(*args, **kwargs)


class UserAgent(models.Model):
    browser = models.TextField()
    operating_system = models.CharField(max_length=50, blank=True)
    operating_version_string = models.CharField(max_length=50, blank=True)
    user_ip_address = models.CharField(max_length=50, blank=True)


class UserAgentCondition(models.Model):
    user_agent = models.ForeignKey(UserAgent, on_delete=models.SET_NULL, blank=True, null=True)
    time_used = models.IntegerField(default=0)

   
class HistoryShorten(models.Model):
    user_agent = models.ForeignKey(UserAgent, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
    shortend_url = models.ForeignKey(ShortenURL, on_delete=models.CASCADE,)
    
    # def __str__(self):
    #     return self.shortend_url
