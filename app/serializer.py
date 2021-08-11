from .models import *
from django.urls import resolve
from rest_framework import serializers
import os
class ArtistSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_photo_url')

    class Meta:
        model = Artist
        fields = ['id', 'name', 'image_url']

    def get_photo_url(self,obj):
        try:
            request = self.context.get('request')
            music_file3 = obj.photo.url
            return request.build_absolute_uri(music_file3)
        except:
            return
class CategorySerializer(serializers.ModelSerializer):
    photo2 = serializers.SerializerMethodField('get_photo_url')
    class Meta:
        model = Category
        fields = ['id', 'title', 'photo2']
    def get_photo_url(self,obj):
        try:
            request = self.context.get('request')
            music_file3 = obj.photo.url
            return request.build_absolute_uri(music_file3)
        except:
            return

class SongSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = serializers.StringRelatedField()
    music_file= serializers.SerializerMethodField("get_music_or_url")
    class Meta:
        model = Song
        fields = ["id","title","artist","category","music_file","likes","date"]
    #  Functions 
    def get_music_or_url(self,obj):
        if obj.url == "":
            request = self.context.get('request')
            music_file3 = obj.music_file2.url
            return music_file3
        else:
            return obj.url