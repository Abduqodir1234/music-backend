from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Artist)

class SongAdmin(admin.ModelAdmin):
    search_fields = ["title"]
admin.site.register(Song,SongAdmin)


# Register your models here.
