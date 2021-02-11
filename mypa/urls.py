"""mypa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals, absolute_import
from . import views

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from .authentication.views import UserViewSet
from .authentication import urls as authentication_urls
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'users', UserViewSet)

schema_view = get_swagger_view(title='mypa APIs')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',auth_views.login ,name="login"),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'logout/$',auth_views.logout,{'next_page' : 'login'}, name="logout"),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^',include('mypa.audio_recorder.urls')),
    url(r'^swagger/$', schema_view),
    url(r'^api/v1/', include(authentication_urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^healthcheck/$', views.health_check),
    url(r'^summary/$', views.show_summary, name="summary"),
    url(r'^get_processed_data/$', views.get_processed_data, name="processed_data"),
    url(r'^get_entity/$', views.get_entity, name="entity"),
    url(r'^send_email/$',views.send_email, name = "email"),
    url(r'^dialogflow_chat/$',views.dialog, name = "dialog"),

    # url(r'^dashboard',views.dashboard,name="dashboard"),
]
