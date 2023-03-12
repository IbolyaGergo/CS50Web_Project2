from django.contrib import admin
from .models import User, ListingModel

class ListingModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img', 'start_bid', 'created_at')

# Register your models here.
admin.site.register(User)
admin.site.register(ListingModel, ListingModelAdmin)