from .models import *
from rest_framework import serializers


class ArtistSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Artist
        fields = ['id', 'name', 'photo']


class CategorySerializer(serializers.ModelSerializer):
    # photo = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Category
        fields = ['id', 'title', 'photo']


class SongSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = serializers.StringRelatedField()

    class Meta:
        model = Song
        fields = ['title', 'category', 'artist', 'music_file', 'likes', 'date']
