from app.views import YoutubeMusicInfo2
from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(YoutubeMusicInfo)
# Register your models here.
