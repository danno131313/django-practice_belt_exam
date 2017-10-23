from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users/create$', views.create_user),
    url(r'^login$', views.login),
    url(r'^show$', views.show),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)/show', views.show_one),
    url(r'^users/(?P<id>\d+)/create_comment', views.create_comment),
]
