from django.urls import path
from downloader.views import index, download

urlpatterns = [
    path('', index),
    path('download/', download, name="download")
]