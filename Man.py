import urllib.request
import urllib.parse
import re
import youtube_dl
import shutil
import os
import send2trash
def main():

    file = open("music.txt", "r")
    readFile = file.read()
    maybeDone = readFile.split("\n")
    songs = len(maybeDone)
    i = 0
    for i in range(songs):    
    #Gui
        #import tkinter as tk
        #from tkinter.simpledialog import askstring
        #root = tk.Tk()
        # show askstring dialog without the Tkinter window
        #root.withdraw()
        #video = askstring("Song", "Enter Song")
        #print(video)
        #Rerun break
        #if video == None:
           # break
    #Finding the video   
        song = maybeDone[i]
        query_string = urllib.parse.urlencode({"search_query" : song})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        video = ("http://www.youtube.com/watch?v=" + search_results[0])
    #Naming the video
        ydl = youtube_dl.YoutubeDL()
        r = None
        with ydl:
            r = ydl.extract_info(video, download=False)  

        title = r['title']
    #Downloading the video
        options = {
            'format': 'bestaudio/best',
            'extractaudio' : True,  # only keep the audio
            'audioformat' : "mp3",  # convert to mp3 
            'outtmpl': title + '.mp3',    # name the file the ID of the video
            'noplaylist' : True,    # only download single song, not playlist
            }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video])
    #Moves the files to a set location
        source = os.listdir(os.path.dirname(os.path.realpath(__file__)))
        destination = (os.path.join(os.path.expandvars("%userprofile%"),"Music"))
        for files in source:
            if files.endswith(".mp3"):
                shutil.copy(files,destination)
    #Deletes the file
        send2trash.send2trash(title + ".mp3")
    return
        
main()

