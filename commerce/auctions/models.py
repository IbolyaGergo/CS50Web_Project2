from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ListingModel(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to = "images/")
    start_bid = models.DecimalField(max_digits=64, decimal_places=2)

    def __str__(self):
        return f"{self.title}, starting bid:${self.start_bid}"
    
