from django.http.response import FileResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import filters


class CategoryApiView(APIView):
    serializers = CategorySerializer

    def get(self, request, format=None):
        category = Category.objects.all().order_by('-id')
        serializer = self.serializers(category, many=True)
        return Response(serializer.data)

# Create your views here.


class ArtistApiView(APIView):
    serializers = ArtistSerializer

    def get(self, request, format=None):
        category = Artist.objects.all().order_by('name')
        serializer = self.serializers(category, many=True)
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
    response = FileResponse(open(filename, 'rb'))
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
