# Generated by Django 3.2 on 2021-08-11 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_song_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='music_file',
            new_name='music_file2',
        ),
    ]
