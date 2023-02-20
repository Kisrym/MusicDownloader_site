from django.urls import path
from downloader.views import index, download, youtube

urlpatterns = [
    path('', index, name="index"),
    path('download/<str:cond>', download, name="download"),
    path('youtube/', youtube, name="youtube"),
]   