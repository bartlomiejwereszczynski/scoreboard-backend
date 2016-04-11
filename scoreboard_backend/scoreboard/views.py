from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Player, Mobile
from .serializers import PlayerSerializer, ProfileSerializer


# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk=None, **kwargs):
        mobile = get_object_or_404(Mobile, uuid=pk)
        player = mobile.player
        serializer = PlayerSerializer(player)
        return Response(serializer.data)
