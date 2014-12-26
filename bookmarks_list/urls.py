from django.conf.urls import url

from bookmarks_list import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<list_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<list_id>\d+)/add_link/$', views.add_link, name='add_link'),
    url(r'^(?P<link_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^add/$', views.add, name='add'),
    url(r'^login/$', views.loginPerson, name='loginPerson'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logoutPerson, name='logoutPerson'),
]