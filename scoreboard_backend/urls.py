"""scoreboard_backend URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers, serializers, viewsets

from scoreboard_backend.scoreboard.views import PlayerViewSet, ProfileViewSet, GoalViewSet, MatchViewSet, index

router = routers.DefaultRouter()
router.register(r'^users', PlayerViewSet)
router.register(r'^profile', ProfileViewSet, base_name="profile")
router.register(r'^goal', GoalViewSet, base_name="goal")
router.register(r'^match', MatchViewSet, base_name="match")

urlpatterns = [
    url(r'^$', index),
    url(r'^api/v1/', include(router.urls)),
    # api/bt_confirm
    # api/user_confirm
    # api/user_add
    # api/users (lista userow do wybory dla frontendu)
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
