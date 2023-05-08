from django.contrib import admin
from .models import User, ListingModel, BidModel, CategoryModel, CommentModel


@admin.action(description="Make selected linsings active")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description="Make selected linsings inactive")
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


class ListingModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img', 'start_bid', 'creator', 'created_at', 'active', 'category')
    actions = [make_active, make_inactive]

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('creator_name', 'body', 'listing', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ListingModel, ListingModelAdmin)
admin.site.register(BidModel)
admin.site.register(CategoryModel, CategoryModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)