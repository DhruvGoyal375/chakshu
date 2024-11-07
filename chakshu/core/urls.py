from django.urls import path

from .views import ProcessOptionView, SearchResultsView, SelectLinkView

urlpatterns = [
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("select/", SelectLinkView.as_view(), name="select_link"),
    path("process/", ProcessOptionView.as_view(), name="process_option"),
]
