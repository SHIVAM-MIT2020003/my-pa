from . import views
from .. import views as main_views
from django.conf.urls import url


urlpatterns = [
    url(r'^homepage/(?P<id>[\w\-]+)/$', views.homepage, name='homepage'),
    # url(r'^homepage/(?P<string>[\w\-]+)/$', views.homepage, name='event_specific'),
    url(r'^store_mp3', views.store_mp3, name='store mp3'),
    url(r'^$', main_views.dashboard, name='dashboard'),
]
