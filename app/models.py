from django.db import models
from django.db.models.fields import URLField
# Create your models here.


class Artist(models.Model):
    name = models.CharField('Ismi', max_length=50)
    photo = models.ImageField(null=True, blank=True)
    likes = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField('kategoriya', max_length=50, blank=True)
    photo = models.ImageField('photo', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Song(models.Model):
    title = models.CharField('Nomi(Artist bilan)', max_length=100000)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.SET_NULL, null=True, blank=True)
    music_file2 = models.FileField(
        'Musiqa Fayli', upload_to='musics', blank=True)
    likes = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(blank=True)

    def __str__(self):
        return self.title
