from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    # path("captioner/", include("captioner.urls")),
]
