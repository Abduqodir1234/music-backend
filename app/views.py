from os import error
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
from django.db.models import Q

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


from rest_framework.pagination import PageNumberPagination
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100000000

class songswithartists(APIView):
    pagination_class = LargeResultsSetPagination
    def get(request, pk=None):
        artist = Artist.objects.get(id=pk)
        queryset = Song.objects.filter(artist=artist)
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchAPIView(generics.ListAPIView):
    search_fields = ['^title', '^artist__name', '^category__title']
    filter_backends = (filters.SearchFilter,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    

@api_view(['GET'])
def download(request, id):
    try:
        obj = Song.objects.get(id=id)
        if(obj.url == ""):
            filename = obj.music_file2
            url = ""
            if(request.META["SERVER_PROTOCOL"].startswith("HTTP")):
                url = "http://" + request.META["HTTP_HOST"]
            else:
                url = "https://" + request.META["HTTP_HOST"]
            url = url + filename.url
            return Response({"url":url})
            # return FileResponse(open(filename,"rb"),as_attachment=True)
        else:
            video =obj.url
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with YoutubeDL(ydl_opts) as ydl: 
                x = ydl.extract_info(video,download=False)
                a = {}
                for i in x["formats"]:
                    if i.get("ext")== "m4a":
                        a = i
                return Response({"url":a.get("url")})
    except:
        obj = Song.objects.get(id=id)
        if(obj.url == ""):
            filename = obj.music_file2
            url = ""
            if(request.META["SERVER_PROTOCOL"].startswith("HTTP")):
                url = "http://" + request.META["HTTP_HOST"]
            else:
                url = "https://" + request.META["HTTP_HOST"]
            url = url + filename.url
            return Response({"url":url})
            # return FileResponse(open(filename,"rb"),as_attachment=True)
        else:
            video ="https://www.youtube.com/watch?v=CDd5EGVB2X0"
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with YoutubeDL(ydl_opts) as ydl: 
                x = ydl.extract_info(video,download=False)
                a = {}
                for i in x["formats"]:
                    if i.get("ext")== "m4a":
                        a = i
                return Response({"url":a.get("url")})


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
# ---------------------------------Unneseccessary View -----------------------------
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
#---------------------------Unneseccessary View -------------------------------- 
class YoutubeMusicInfo2(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self,request):
        video = "https://www.youtube.com/watch?v=EEhKF3Qc1Bw"
        ydl_opts = {
            'format': 'bestaudio/best',
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
        }
        with YoutubeDL(ydl_opts) as ydl: 
            x = ydl.extract_info(video,download=False)
            a = {}
            for i in x["formats"]:
                print(type(i))
                if i.get("ext")== "m4a":
                    a = i
            # video_url = info_dict.get("url", None)
            # video_id = info_dict.get("id", None)
            # video_title = info_dict.get('title', None)
            # print("TItle:",video_title)
            return Response(a)
# -----------------GET CHANNEL URL VIEW------------------------py -m pip install youtube_dl-------
@login_required(login_url="/api/songs")
def get_channel_url(request):
    if request.method == "POST":
        links = []
        video = request.POST.get("youtube_channel_url")
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
                if Song.objects.filter(url = i).exists():
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
                            category = Category.objects.first()
                            artist = Artist.objects.first()
                            if i.startswith("https://www.youtube.com/watch?v="):
                                info_dict = ydl.extract_info(i, download=False)
                                video_title = info_dict.get('title', None)
                                print(video_title)
                                if video_title and i.startswith("https://www.youtube.com/watch?v=") and not (Song.objects.filter(url = i).exists()) :
                                    x = Song.objects.create(url=i,title=video_title,category=category,artist=artist)
                                    x.save()
                        except:
                            print("some problem")
                       
        
        collectLinks()
        driver.quit()
        return redirect("/api/url")
    else:
        return render(request,"demo5.html")

@login_required(login_url="/api/songs")
def get_music(request):
    x = Category.objects.all()
    y = Artist.objects.all()
    if request.method == "POST":
        artist = Artist.objects.get(id = request.POST.get("artist")) or Artist.objects.first()
        title = request.POST.get("title") or "" 
        url = request.POST.get("url") or ""
        music = request.FILES.get("music")
        category = Category.objects.get(id = request.POST["category"])  or Category.objects.first()
        print(category)
        d = Song.objects.create(title = title,artist=artist,url=url,category=category,music_file2=music)
        d.save()
    return render(request,"new one.html",{"x":x,"y":y})



class Search_in_Navbar(APIView):
    def get(self,request):
        try:
            print(request.GET)
            search = request.GET.get("search")
            search1 = search.split(" ")
            search2 = search.split("-")
            for i in search1:
                r2 = Q(title__icontains = i)
            for i in search2:
                r3 = Q(title__icontains = i)
            queryset = Song.objects.filter(r2 | r3)[:7]
            print(queryset)
            serializer = SongSerializer(queryset,many=True)
            return Response(serializer.data)
        except:
            print("error")
            return Response([])
