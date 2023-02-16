from django.shortcuts import render
from downloader.forms import DownloadForms
from django.http import FileResponse
from music_downloader import *
import os
from zipfile import ZipFile
from shutil import rmtree

# Create your views here.
def index(request):
    form = DownloadForms()
    return render(request, 'index.html', {"form" : form})

def download(request):
    form = DownloadForms()

    if request.method == "POST":
        form = DownloadForms(request.POST)

        if form.is_valid():
            spotify = Spotify()

            if "track" in form["link"].value():
                spotify.track(form["link"].value())
            else:
                spotify.playlist(form["link"].value(), offset=77)

            spotify.download()
            
            with ZipFile('musics.zip', 'w') as zf:
                for file in os.listdir("musicas"):
                    zf.write("musicas/" + file)

            rmtree("musicas") # "limpando" a pasta de músicas

            return FileResponse(open('musics.zip', 'rb'), as_attachment = True)
    
    return render(request, "index.html", {"form" : form})