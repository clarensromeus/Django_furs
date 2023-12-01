from django.contrib import admin
from .models import Post

# Register your models here.


class PostModel(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    ordering = ["-created_at"]
    search_fields = ["title"]


admin.site.register(Post, PostModel)
