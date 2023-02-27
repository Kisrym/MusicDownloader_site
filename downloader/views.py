from django.shortcuts import render, redirect
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
            
            # cond == False: Spotify
            # cond == True: Youtube
            try:
                if cond == "False":
                    spotify = Spotify()

                    if "track" in form["link"].value():
                        spotify.track(form["link"].value())

                    elif "playlist" in form["link"].value() and "youtube" not in form["link"].value():
                        spotify.playlist(form["link"].value(), offset=int(form["offset"].value()))
                    
                    else:
                        messages.error(request, "Link inválido")
                        return redirect("index", {"form" : form, "classe" : CLASSE})

                    spotify.download()
                
                elif cond == "True":
                    youtube = Youtube()

                    if "watch" in form["link"].value() or "youtu.be" in form["link"].value():
                        youtube.track(form["link"].value())

                    elif "playlist" in form["link"].value() and "spotify" not in form["link"].value():
                        messages.info(request, "Essa funcionalidade ainda não existe.")

                    else:
                        messages.error(request, "Link inválido")
                        return redirect("index.html", {"form" : form, "classe" : "youtube"})     

                    youtube.download()
                
                with ZipFile('musics.zip', 'w') as zf:
                    for file in os.listdir("musicas"):
                        zf.write("musicas/" + file)

                rmtree("musicas") # "limpando" a pasta de músicas

                return FileResponse(open('musics.zip', 'rb'), as_attachment = True)
            
            except:
                messages.error(request, "Erro no download")
                return redirect("index", {"form" : form, "classe" : CLASSE})
    
    return render(request, "index.html", {"form" : form, "classe" : CLASSE})

def youtube(request):
    form = DownloadForms()
    CLASSE = "youtube"
    
    return render(request, 'index.html', {"form" : form, "classe" : CLASSE})