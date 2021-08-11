from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

song_list = SongView.as_view({'get': 'list'})
song_detail = SongView.as_view({'get': 'retrieve'})
song_like = SongView.as_view({'get': 'post'})

top_musics = Tops.as_view({"get": "topmusic"})
recent_music = Tops.as_view({"get":"recentmusics"})
# top_artists = Tops.as_view({"get": "topartists"})

urlpatterns = [
    path('categories', CategoryApiView.as_view(), name='categories'),
    path('artists', ArtistApiView.as_view(), name='artists'),
    path('songs', song_list, name='lists'),
    path('songs/<int:pk>', song_detail, name='song-detail'),
    path('sons/catgegory/<int:pk>', songswithcategory, name='song-category'),
    path('songs/artist/<int:pk>', songswithartists, name='song-artist'),
    path('music/', SearchAPIView.as_view()),
    path('download/song/<int:id>', download, name='song-download'),
    path('like/song/<int:pk>', song_like, name='song-like'),
    path("top/musics", top_musics),
    path("songs/recent/",recent_music),
    path("gytmc/",YouTubeMusics.as_view()),
    path("gminfo/",YoutubeMusicInfo2.as_view()),
    path("url/",get_channel_url),
    path("music2",get_music)
    # path("top/artists/",top_artists) 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
