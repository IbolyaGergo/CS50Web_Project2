from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class ListingModel(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    start_bid = models.DecimalField(max_digits=64, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    # category = models.CharField(max_length=64)
    category = models.ForeignKey("CategoryModel", on_delete=models.CASCADE, default=1)
    active = models.BooleanField(default=True)
    winner = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}, starting bid:${self.start_bid}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(ListingModel, blank=True)
    # pass

class BidModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=64, decimal_places=2)

    def __str__(self):
        return f"${self.bid}"

class CategoryModel(models.Model):
    name = models.CharField(max_length=64)
    listing = models.ManyToManyField(ListingModel, blank=True)

    def __str__(self):
        return f"{self.name}"
    
class CommentModel(models.Model):
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE, related_name="comments")
    creator_name = models.CharField(max_length=64)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.creator_name}."
