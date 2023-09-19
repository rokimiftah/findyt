from django.db import models


# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=250)
    playlist_id = models.CharField(max_length=250)
    thumbnail_url = models.CharField(max_length=250)
    description = models.TextField()


class Video(models.Model):
    title = models.CharField(max_length=250)
    views = models.IntegerField()
    likes = models.IntegerField()
    youtube_id = models.CharField(max_length=250)
    date_published = models.DateField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
