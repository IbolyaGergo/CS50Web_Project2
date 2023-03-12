from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class ListingModel(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    start_bid = models.DecimalField(max_digits=64, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    # category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}, starting bid:${self.start_bid}"
    
