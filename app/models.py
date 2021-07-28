from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField('Ismi', max_length=50)
    photo = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField('kategoriya', max_length=50)
    photo = models.ImageField('photo', )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Song(models.Model):
    title = models.CharField('nomi', max_length=50)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    artist = models.ForeignKey(Artist,on_delete=models.SET_NULL,null=True)
    music_file = models.FileField('Musiqa Fayli', upload_to='musics',)
    likes = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.title, self.artist)




