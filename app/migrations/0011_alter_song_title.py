# Generated by Django 3.2 on 2021-08-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_song_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nomi(Artist bilan)'),
        ),
    ]
