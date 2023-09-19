import requests
from celery import shared_task
from django.conf import settings

from findyt.models import Channel, Video


@shared_task(bind=True)
def get_video_stats(self):
    Video.objects.all().delete()

    channels = Channel.objects.all()
    channel_ids = ",".join([channel.playlist_id for channel in channels])

    url = f"""
        https://www.googleapis.com/youtube/v3/playlists?
        id={channel_ids}
        &part=contentDetails
        &key={settings.YOUTUBE_API_KEY}
    """
    res = requests.get(url)

    total_requests = 0

    for item in res.json()["items"]:
        total_requests += int(item["contentDetails"]["itemCount"])

    for channel in channels:
        playlist_api_url = f"""
        https://www.googleapis.com/youtube/v3/
            playlists?id={channel.playlist_id}
            &part=snippet
            &maxResults=50
            &key={settings.YOUTUBE_API_KEY}
        """

        while True:
            playlist_res = requests.get(playlist_api_url)
            results = playlist_res.json()
            videos_ids = []

            for item in results:
                videos_ids.append(item["snippet"]["resourceId"]["videoId"])
            video_ids_string = ",".join(videos_ids)

            video_api_url = f"""
                https://www.googleapis.com/youtube/v3/
                videos?id={video_ids_string}
                &part=snippet,statistics
                &key={settings.YOUTUBE_API_KEY}
            """
            videos_res = requests.get(video_api_url)

            for item in videos_res.json():
                video = Video(
                    title=item["snippet"]["title"],
                    views=item["statistics"]["viewCount"],
                    likes=item["statistics"]["likeCount"],
                    youtube_id=item["id"],
                    date_published=item["snippet"]["publishedAt"],
                    channel=channel,
                )
                video.save()

            if "nextPageToken" in results:
                playlist_api_url = f"""
                    https://www.googleapis.com/youtube/v3/
                    playlists?id={channel.playlist_id}
                    &part=snippet
                    &maxResults=50
                    &key={settings.YOUTUBE_API_KEY}
                    &pageToken={results['nextPageToken']}
                """
            else:
                break
