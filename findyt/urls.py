from django.urls import path

from findyt.views import index

urlpatterns = [
    path("", index, name="index"),
]
