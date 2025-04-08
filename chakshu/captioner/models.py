# Create your models here.
from django.db import models
class WikipediaPage(models.Model):
    url = models.URLField(unique=True)
    title = models.TextField()  # Increased max_length
    created_at = models.DateTimeField(auto_now_add=True)

class ImageCaption(models.Model):
    page = models.ForeignKey(WikipediaPage, on_delete=models.CASCADE, related_name='captions')
    image_url = models.URLField(max_length=1024)  # Increased max_length
    final_caption = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('page', 'image_url')

    def __str__(self):
        return f"{self.page.title} - {self.image_url}"