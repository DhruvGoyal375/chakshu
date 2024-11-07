from django.urls import path

from .views import WikiSummaryScraper

urlpatterns = [
    path("summary/", WikiSummaryScraper.as_view(), name="wiki_summary_scraper"),
]
