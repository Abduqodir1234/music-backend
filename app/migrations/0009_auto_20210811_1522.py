# Generated by Django 3.2 on 2021-08-11 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_youtubechannelurls_youtubemusicinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='YouTubeChannelUrls',
        ),
        migrations.DeleteModel(
            name='YoutubeMusicInfo',
        ),
        migrations.RemoveField(
            model_name='song',
            name='photo',
        ),
        migrations.AddField(
            model_name='song',
            name='url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='music_file',
            field=models.FileField(blank=True, upload_to='musics', verbose_name='Musiqa Fayli'),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Nomi(Artist bilan)'),
        ),
    ]
