from django.conf.urls import url
from django.contrib import admin
from views import ReservationAPI, serve_app
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    (url('app', serve_app)),
    (url("^(?P<uuid>[A-Za-z0-9-]*)$", ReservationAPI.as_view())),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)