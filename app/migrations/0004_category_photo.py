# Generated by Django 3.2.5 on 2021-07-14 12:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210712_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='', verbose_name='photo'),
            preserve_default=False,
        ),
    ]
