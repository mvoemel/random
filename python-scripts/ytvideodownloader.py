from pytube import YouTube
from sys import argv

#paste the url of the video you want to download in the following line
url = "https://www.youtube.com/watch?v=XXXXXXXXX"
yt = YouTube(url)

print("Title: " + yt.title)
print("Url: " + url)

yd = yt.streams.get_highest_resolution()

yd.download('/YOUR/DOWNLOAD/PATH')