from django.contrib import admin
from .models import User, ListingModel, BidModel

class ListingModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img', 'start_bid', 'creator', 'created_at')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ListingModel, ListingModelAdmin)
admin.site.register(BidModel)