# Generated by Django 3.2 on 2021-07-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_artist_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
