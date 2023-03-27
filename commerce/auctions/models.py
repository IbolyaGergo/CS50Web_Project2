from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class ListingModel(models.Model):
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    start_bid = models.DecimalField(max_digits=64, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    # category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}, starting bid:${self.start_bid}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(ListingModel, blank=True, related_name="watcher")
    # pass

class BidModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE, related_name="listing")
    bid = models.DecimalField(max_digits=64, decimal_places=2)

    def __str__(self):
        return f"${self.bid}"
