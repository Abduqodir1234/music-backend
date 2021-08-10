from django.conf.urls import url
from django.http import request
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from youtube_dl import YoutubeDL
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.decorators import permission_required,login_required
class CategoryApiView(APIView):
    serializers = CategorySerializer

    def get(self, request, format=None):
        #First Category Musics
        first = Category.objects.all()
        queryset = Song.objects.filter(category=first[0])
        serializer2 = SongSerializer(queryset, many=True)
        #---------------------------
        category = first.order_by('-id')
        serializer = self.serializers(category, many=True)
        return Response({"category":serializer.data,"music":serializer2.data,"category_name":first[0].title})

# Create your views here.
class ArtistApiView(APIView):
    serializers = ArtistSerializer

    def get(self, request, format=None):
        artist = Artist.objects.all().order_by('name')
        serializer = self.serializers(artist, many=True)
        return Response(serializer.data)

class SongView(viewsets.ViewSet):
    serilize = SongSerializer
    model = Song.objects.all().order_by('-id')

    def list(self, request):
        serializer = self.serilize(self.model, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Song.objects.all()
        song = get_object_or_404(queryset, pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def post(self, request, pk=None):
        queryset = Song.objects.all()
        song = get_object_or_404(queryset, pk=pk)
        song.likes += 1
        song.save()
        return Response({'status': 'ok'})

@api_view(['GET'])
def songswithcategory(request, pk=None):
    category = Category.objects.get(id=pk)

    queryset = Song.objects.filter(category=category)
    serializer = SongSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def songswithartists(request, pk=None):
    artist = Artist.objects.get(id=pk)
    queryset = Song.objects.filter(artist=artist)
    serializer = SongSerializer(queryset, many=True)
    return Response(serializer.data)

class SearchAPIView(generics.ListCreateAPIView):
    search_fields = ['^title', '^artist__name', '^category__title']
    filter_backends = (filters.SearchFilter,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer

@api_view(['GET'])
def download(request, id):
    obj = Song.objects.get(id=id)
    filename = obj.music_file.path
    response = FileResponse(open(filename, 'rb'),as_attachment = True)
    return response

class Tops(viewsets.ViewSet):
    def topmusic(request, self):
        obj = Song.objects.all().order_by("-likes")[:10]
        serializer = SongSerializer(obj, many=True)
        return Response(serializer.data)

    def topartists(self, request):
        obj = Artist.objects.all().order_by("likes")[:10]
        serializer = ArtistSerializer(obj,many=True)
        return Response(serializer.data)
    def recentmusics(self,request):
        obj = Song.objects.all().order_by("-date","-likes")[:10]
        serializer = SongSerializer(obj,many=True)
        return Response(serializer.data)
class YouTubeMusics(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = ""
    permission_classes = [permissions.IsAdminUser]
    def post(self,request):
        links = []
        driver = webdriver.Chrome("C:\\chromedriver.exe")
        driver.get('https://www.youtube.com/c/RizaNovaUZ/videos')
        def collectLinks():
            while True:
                prev_ht=driver.execute_script("return document.documentElement.scrollHeight;")
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                ht=driver.execute_script("return document.documentElement.scrollHeight;")
                if prev_ht==ht:
                    break
            elements = []
            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                elements.append(str(elem.get_attribute("href")))

            for i in elements:
                 
                f = open("document.txt","a")
                f.write(i + "\n")
                f.close()

        collectLinks()
        driver.quit()
        return redirect("/api/songs")
class YoutubeMusicInfo2(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self,request):
        video = "https://www.youtube.com/watch?v=EEhKF3Qc1Bw"
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video, download=False)
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            print("TItle:",video_title)
            return Response({"salom":"salom"})

@login_required(login_url="/api/songs")
@permission_required("YoutubeMusicInfo.add_choice")
def get_channel_url(request):
    if request.method == "POST":
        links = []
        video = request.POST["youtube_channel_url"]
        driver = webdriver.Chrome("C:\\chromedriver.exe")
        driver.get(video)
        def collectLinks():
            while True:
                prev_ht=driver.execute_script("return document.documentElement.scrollHeight;")
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                ht=driver.execute_script("return document.documentElement.scrollHeight;")
                if prev_ht==ht:
                    break
            elements = []
            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                elements.append(str(elem.get_attribute("href")))

            for i in elements:
                if YoutubeMusicInfo.objects.filter(url = i).exists():
                    pass
                else:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                    with YoutubeDL(ydl_opts) as ydl:
                        try:
                            if i.startswith("https://www.youtube.com/watch?v="):
                                info_dict = ydl.extract_info(i, download=False)
                                video_title = info_dict.get('title', None)
                                print(video_title)
                                if video_title and i.startswith("https://www.youtube.com/watch?v="):
                                    x = YoutubeMusicInfo.objects.create(url=i,name=video_title)
                                    x.save()
                        except:
                            print("some problem")
                       
        
        collectLinks()
        driver.quit()
        return redirect("/api/url")
    return render(request,"demo5.html")