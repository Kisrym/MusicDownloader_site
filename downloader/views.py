from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib import messages
from downloader.forms import DownloadForms
from music_downloader.music_downloader import *
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

    if os.path.isdir("musicas"):
        rmtree("musicas") # "limpando" a pasta de músicas
        
    if request.method == "POST":
        form = DownloadForms(request.POST)
        
        if form.is_valid():
            # cond == False: Spotify
            # cond == True: Youtube
            BASE_DIR = os.getcwd()
            IS_ZIP = False

            try:
                if cond == "False":
                    spotify = Spotify(BASE_DIR)

                    if "track" in form["link"].value():
                        spotify.track(form["link"].value())

                    elif "playlist" in form["link"].value() and "youtube" not in form["link"].value():
                        if form["offset"].value() == "" or form["offset"].value() == 0:
                            offset = 1
                        
                        TOTAL = spotify.get_playlist_total(form["link"].value())

                        if form["limit"].value() == "":
                            limit = 50 if TOTAL > 50 else TOTAL # se o total de músicas for maior que 50, o limite vai ser 50

                        spotify.playlist(form["link"].value(), offset = offset, limit = limit)
                        IS_ZIP = True
                    
                    else:
                        messages.error(request, "Link inválido")
                        return redirect("index", {"form" : form, "classe" : CLASSE})

                    spotify.download()
                
                elif cond == "True":
                    youtube = Youtube(BASE_DIR)

                    if "watch" in form["link"].value() or "youtu.be" in form["link"].value():
                        youtube.track(form["link"].value())

                    elif "playlist" in form["link"].value() and "spotify" not in form["link"].value():
                        if form["offset"].value() == "":
                            offset = 1

                        TOTAL = youtube.get_playlist_total(form["link"].value())

                        if form["limit"].value() == "":
                            limit = 50 if TOTAL > 50 else TOTAL # se o total de músicas for maior que 50, o limite vai ser a metade dele
                        
                        youtube.playlist(form["link"].value(), offset = offset, limit = limit)
                        IS_ZIP = True

                    else:
                        messages.error(request, "Link inválido")
                        return redirect("index.html", {"form" : form, "classe" : "youtube"})     

                    youtube.download()
                
                if IS_ZIP:
                    with ZipFile('musics.zip', 'w') as zf:
                        for file in os.listdir("musicas"):
                            zf.write("musicas/" + file, "musicas/" + file) # mudando o diretório interno do Zip

                    return FileResponse(open('musics.zip', 'rb'), as_attachment = True)
                
                else:
                    for file in os.listdir("musicas"):
                        if file.endswith(".mp3"):
                            return FileResponse(open(f"musicas/{file}", 'rb'), as_attachment = True)
            
            except:
                messages.error(request, "Erro no download")
                return redirect("index", {"form" : form, "classe" : CLASSE})
    
    return render(request, "index.html", {"form" : form, "classe" : CLASSE})

def youtube(request):
    form = DownloadForms()
    CLASSE = "youtube"
    
    return render(request, 'index.html', {"form" : form, "classe" : CLASSE})