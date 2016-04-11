from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .models import Player, Mobile, Match, Goal
from .serializers import PlayerSerializer, ProfileSerializer, GoalSerializer, MatchSerializer, ConfirmSerializer


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


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def retrieve(self, request, pk=None, **kwargs):
        if pk == "current":
            match = get_object_or_404(Match, state__in=[Match.STATE_ACTIVE, Match.STATE_WAITING])
        else:
            match = get_object_or_404(Match, pk=pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def confirm(self, request, pk=None, **kwargs):
        match = self.get_object()
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(match=match)

        return Response(MatchSerializer(instance=match).data)
