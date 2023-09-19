from django.urls import path

from findyt.views import add_channel, generate, index, search_channel

urlpatterns = [
    path("", index, name="index"),
    path("search-channel/", search_channel, name="search-channel"),
    path("add-channel/<channel_id>/", add_channel, name="add-channel"),
    path("generate/", generate, name="generate"),
]
