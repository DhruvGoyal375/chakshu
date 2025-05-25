# Register your models here.
from django.contrib import admin

from .models import ImageCaption, WikipediaPage


@admin.register(WikipediaPage)
class WikipediaPageAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "created_at")
    search_fields = ("title", "url")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(ImageCaption)
class ImageCaptionAdmin(admin.ModelAdmin):
    list_display = ("page", "image_url", "created_at")
    search_fields = ("image_url", "final_caption")
    list_filter = ("created_at", "page")
    ordering = ("-created_at",)
