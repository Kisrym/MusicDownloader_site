from django.shortcuts import render
from django.http import FileResponse
from django.contrib import messages
from downloader.forms import DownloadForms
from music_downloader import *
import os
from zipfile import ZipFile
from shutil import rmtree

CLASSE = "spotify"

# Create your views here.
def index(request):
    form = DownloadForms()
    return render(request, 'index.html', {"form" : form, "classe" : CLASSE})

def download(request, cond):
    form = DownloadForms()

    if request.method == "POST":
        form = DownloadForms(request.POST)

        if form.is_valid():
            
            if cond == "True":
                print("youtube")
            elif cond == "False":
                print("spotify")
            
            if cond == "False":
                spotify = Spotify()

                if "track" in form["link"].value():
                    spotify.track(form["link"].value())

                elif "playlist" in form["link"].value():
                    spotify.playlist(form["link"].value(), offset=int(form["offset"].value()))

                spotify.download()
            
            elif cond == "True":
                youtube = Youtube()
                if "watch" in form["link"].value():
                    youtube.track(form["link"].value())
                else:
                    messages.error("erro")

                youtube.download()
            
            with ZipFile('musics.zip', 'w') as zf:
                for file in os.listdir("musicas"):
                    zf.write("musicas/" + file)

            rmtree("musicas") # "limpando" a pasta de músicas

            return FileResponse(open('musics.zip', 'rb'), as_attachment = True)
    
    return render(request, "index.html", {"form" : form, "classe" : CLASSE})

def youtube(request):
    form = DownloadForms()
    CLASSE = "youtube"
    
    return render(request, 'index.html', {"form" : form, "classe" : CLASSE})