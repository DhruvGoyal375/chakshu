# Create your models here.
from django.db import models


class WikipediaPage(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ImageCaption(models.Model):
    page = models.ForeignKey(WikipediaPage, on_delete=models.CASCADE, related_name="captions")
    image_url = models.URLField()
    final_caption = models.TextField()  # Store the final LLaVA caption
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("page", "image_url")

    def __str__(self):
        return f"{self.page.title} - {self.image_url}"
