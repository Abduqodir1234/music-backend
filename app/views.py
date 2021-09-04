from django.core import paginator
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
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
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from pytube import Channel
from pytube import YouTube
from django.db.models import Q



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


class CustomPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            "current_page_number": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            'results': data,

        })

class CategoryApiView(APIView):
    serializers = CategorySerializer

    def get(self, request, format=None):
        # First Category Musics
        first = Category.objects.all()
        category = first.order_by('-id')
        serializer = self.serializers(category, many=True)
        return Response({
            "category": serializer.data,
            })
    def post(self,request,pk=None):
        x = get_object_or_404(Category,pk = pk)
        x.likes +=1
        x.save()
        return Response({"status":"Successfully completed"})


@api_view(['GET'])
def songswithcategory(request, pk=None):
    paginator = CustomPagination()
    category = Category.objects.get(id=pk)
    queryset = Song.objects.filter(category=category)
    result = paginator.paginate_queryset(queryset, request)
    serializer = SongSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def songswithartists(request, pk=None):
    paginator = CustomPagination()
    paginator.page_size = 20
    artist = Artist.objects.get(id=pk)
    queryset2 = Song.objects.filter(artist=artist)
    result = paginator.paginate_queryset(queryset2, request)
    serializer = SongSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


class SearchAPIView(APIView):
    def get(self, request):
        try:
            paginator = CustomPagination()
            search = request.GET.get("search")
            search1 = search.split(" ")
            search2 = search.split("-")
            for i in search1:
                r2 = Q(title__icontains=i)
            for i in search2:
                r3 = Q(title__icontains=i)
            queryset = Song.objects.filter(r2 | r3)
            result = paginator.paginate_queryset(queryset, request)
            serializer = SongSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        except:
            print("error")
            return Response([])


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
            return Response({"url": url})
            # return FileResponse(open(filename,"rb"),as_attachment=True)
        else:
            video = obj.url
            c = YouTube(video)
            w = c.streams.filter(only_audio=True)

            return Response({"url": w[0].url})
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
            return Response({"url": url})
            # return FileResponse(open(filename,"rb"),as_attachment=True)
        else:
            video = "https://www.youtube.com/watch?v=CDd5EGVB2X0"
            c = YouTube(video)
            w = c.streams.filter(only_audio=True)

            return Response({"url": w[0].url})


class Tops(viewsets.ViewSet):
    def topmusic(request, self):
        obj = Song.objects.all().order_by("-likes")[:10]
        serializer = SongSerializer(obj, many=True)
        return Response(serializer.data)

    def topartists(self, request):
        obj = Artist.objects.all().order_by("likes")[:10]
        serializer = ArtistSerializer(obj, many=True)
        return Response(serializer.data)

    def recentmusics(self, request):
        obj = Song.objects.all().order_by("-date", "-likes")[:10]
        serializer = SongSerializer(obj, many=True)
        return Response(serializer.data)


@login_required(login_url="/api/songs")
def get_channel_url(request):
    x = Category.objects.all()
    y = Artist.objects.all()
    if request.method == "POST":
        links = []
        print('Files:', request.FILES)
        print("POST:", request.POST)
        channel_url = request.POST.get("youtube_channel_url")
        category_name = request.POST.get("category")
        category_image = request.FILES.get("category_image")
        artist_name = request.POST.get("artist")
        artist_image = request.FILES.get("artist_image")
        r = Channel(channel_url)
        if Category.objects.filter(title=category_name).exists():
            category = Category.objects.get(
                title=category_name)
        else:
            category = Category.objects.create(
                title=category_name, photo=category_image)
            category.save()
        if Artist.objects.filter(name=artist_name).exists():
            artist = Artist.objects.get(
                name=artist_name)
        else:
            artist = Artist.objects.create(
                name=artist_name, photo=artist_image)
            artist.save()
        for i in r.video_urls:
            try:
                r = YouTube(i)
                video_title = r.title
                print(video_title)
                x = Song.objects.create(
                    url=i, title=video_title, category=category, artist=artist)
                x.save()
            except:
                print("some problem")
        return redirect("/api/url")
    else:
        return render(request, "demo5.html", {"x": x, "y": y})


@login_required(login_url="/api/songs")
def get_music(request):
    x = Category.objects.all()
    y = Artist.objects.all()
    if request.method == "POST":
        category_name = request.POST.get("category")
        category_image = request.FILES.get("category_image")
        artist_name = request.POST.get("artist")
        artist_image = request.FILES.get("artist_image")
        if Category.objects.filter(title=category_name).exists():
            category = Category.objects.get(
                title=category_name)
        else:
            category = Category.objects.create(
                title=category_name, photo=category_image)
            category.save()
        if Artist.objects.filter(name=artist_name).exists():
            artist = Artist.objects.get(
                name=artist_name)
        else:
            artist = Artist.objects.create(
                name=artist_name, photo=artist_image)
            artist.save()
        title = request.POST.get("title") or ""
        url = request.POST.get("url") or ""
        music = request.FILES.get("music")
        d = Song.objects.create(
            title=title, artist=artist, url=url, category=category, music_file2=music)
        d.save()
    return render(request, "new one.html", {"x": x, "y": y})


class Search_in_Navbar(APIView):
    def get(self, request):
        try:
            print(request.GET)
            search = request.GET.get("search")
            search1 = search.split(" ")
            search2 = search.split("-")
            for i in search1:
                r2 = Q(title__icontains=i)
            for i in search2:
                r3 = Q(title__icontains=i)
            queryset = Song.objects.filter(r2 | r3)[:7]
            serializer = SongSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            print("error")
            return Response([])
class Playlist_Musics(APIView):
    def post(self,request):
        ids2 = request.data.get("array")
        if ids2:
            ids = ids2.split(",")
            # r = []
            t = "SELECT * FROM app_song WHERE"
            for count,i in enumerate(ids):
                # r.append(Q(id = int(i)))
                if count == 0:
                    t += f' id={int(i)}'
                else: 
                    t += f' or id={int(i)}'
            r = Song.objects.raw(t)
            paginator = CustomPagination()
            queryset = paginator.paginate_queryset(r,request)
            serializer = SongSerializer(queryset,many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response([])
  # def collectLinks():
        #     while True:
        #         prev_ht = driver.execute_script(
        #             "return document.documentElement.scrollHeight;")
        #         driver.execute_script(
        #             "window.scrollTo(0, document.documentElement.scrollHeight);")
        #         time.sleep(2)
        #         ht = driver.execute_script(
        #             "return document.documentElement.scrollHeight;")
        #         if prev_ht == ht:
        #             break
        #     elements = []
        #     elems = driver.find_elements_by_xpath("//a[@href]")
        #     for elem in elems:
        #         elements.append(str(elem.get_attribute("href")))

        #     for i in elements:
        #         if Song.objects.filter(url=i).exists():
        #             pass
        #         else:
        #             ydl_opts = {
        #                 'format': 'bestaudio/best',
        #                 'postprocessors': [{
        #                     'key': 'FFmpegExtractAudio',
        #                     'preferredcodec': 'mp3',
        #                     'preferredquality': '192',
        #                 }],
        #             }
        #             with YoutubeDL(ydl_opts) as ydl:
        #                 try:
        #                     if Category.objects.filter(title=category_name).exists():
        #                         category = Category.objects.get(
        #                             title=category_name)
        #                     else:
        #                         category = Category.objects.create(
        #                             title=category_name, photo=category_image)
        #                         category.save()
        #                     if Artist.objects.filter(name=artist_name).exists():
        #                         artist = Artist.objects.get(
        #                             name=artist_name)
        #                     else:
        #                         artist = Artist.objects.create(
        #                             name=artist_name, photo=artist_image)
        #                         artist.save()
        #                     if i.startswith("https://www.youtube.com/watch?v="):
        #                         info_dict = ydl.extract_info(i, download=False)
        #                         video_title = info_dict.get('title', None)
        #                         print(video_title)
        #                         if video_title and i.startswith("https://www.youtube.com/watch?v=") and not (Song.objects.filter(url=i).exists()):
        #                             x = Song.objects.create(
        #                                 url=i, title=video_title, category=category, artist=artist)
        #                             x.save()
        #                 except:
        #                     print("some problem")

        # collectLinks()
        # driver.quit()
# ---------------------------------Unneseccessary View -----------------------------


# class YouTubeMusics(APIView):
#     template_name = ""
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request):
#         links = []
#         driver = webdriver.Chrome("C:\\chromedriver.exe")
#         driver.get('https://www.youtube.com/c/RizaNovaUZ/videos')

#         def collectLinks():
#             while True:
#                 prev_ht = driver.execute_script(
#                     "return document.documentElement.scrollHeight;")
#                 driver.execute_script(
#                     "window.scrollTo(0, document.documentElement.scrollHeight);")
#                 time.sleep(2)
#                 ht = driver.execute_script(
#                     "return document.documentElement.scrollHeight;")
#                 if prev_ht == ht:
#                     break
#             elements = []
#             elems = driver.find_elements_by_xpath("//a[@href]")
#             for elem in elems:
#                 elements.append(str(elem.get_attribute("href")))

#             for i in elements:

#                 f = open("document.txt", "a")
#                 f.write(i + "\n")
#                 f.close()

#         collectLinks()
#         driver.quit()
#         return redirect("/api/songs")
# # ---------------------------Unneseccessary View --------------------------------


# class YoutubeMusicInfo2(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         video = "https://www.youtube.com/watch?v=EEhKF3Qc1Bw"
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             # 'postprocessors': [{
#             #     'key': 'FFmpegExtractAudio',
#             #     'preferredcodec': 'mp3',
#             #     'preferredquality': '192',
#             # }],
#         }
#         with YoutubeDL(ydl_opts) as ydl:
#             x = ydl.extract_info(video, download=False)
#             a = {}
#             for i in x["formats"]:
#                 print(type(i))
#                 if i.get("ext") == "m4a":
#                     a = i
#             # video_url = info_dict.get("url", None)
#             # video_id = info_dict.get("id", None)
#             # video_title = info_dict.get('title', None)
#             # print("TItle:",video_title)
#             return Response(a)


# -----------------GET CHANNEL URL VIEW------------------------py - m pip install youtube_dl-------
