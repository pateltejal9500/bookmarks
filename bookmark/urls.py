from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^bookmarks_list/', include('bookmarks_list.urls', namespace="bookmarks_list")),  
)
