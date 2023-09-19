import requests
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from findyt.models import Channel


# Create your views here.
def index(request):
    channels = Channel.objects.all()
    context = {"channels": channels}
    return render(request, "findyt/index.html", context)


def search_channel(request):
    query = request.GET["q"]
    url = f"https://www.googleapis.com/youtube/v3/search?q={query}&type=channel&part=snippet&key={settings.YOUTUBE_API_KEY}"
    res = requests.get(url)
    results = res.json()["items"]
    context = {"results": results}
    return render(request, "findyt/search-results.html", context)


@csrf_exempt
def add_channel(request, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?id={channel_id}&part=snippet,contentDetails&key={settings.YOUTUBE_API_KEY}"
    res = requests.get(url)
    result = res.json()["items"][0]
    channel = Channel(
        name=result["snippet"]["title"],
        playlist_id=result["contentDetails"]["relatedPlaylists"]["uploads"],
        thumbnail_url=result["snippet"]["thumbnails"]["default"]["url"],
        description=result["snippet"]["description"],
    )
    channel.save()
    channels = Channel.objects.all()
    context = {"channels": channels}
    return render(request, "findyt/channels.html", context)
