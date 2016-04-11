from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Player, Mobile, Match, Goal
from .serializers import PlayerSerializer, ProfileSerializer, GoalSerializer, MatchSerializer


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

    def create(self, request, *args, **kwargs):
        match = get_object_or_404(Match, state=Match.STATE_ACTIVE)
        if request["side"] == Goal.SIDE_RED:
            match.goal_red += 1
        else:
            match.goal_blue += 1

        match.save()
        goal, _ = Goal.objects.get_or_create(match=match, side=request["side"])
        serializer = GoalSerializer(goal)

        return Response(serializer.data)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def retrieve(self, request, pk=None, **kwargs):
        if pk == "current":
            match = get_object_or_404(Match, state=Match.STATE_ACTIVE)
        else:
            match = get_object_or_404(Match, pk=pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data)
