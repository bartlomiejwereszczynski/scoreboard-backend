from django.shortcuts import get_object_or_404
from .models import Player, Mobile, Match, Team, Goal

from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(default='')
    confirmed = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('pk', 'username', 'avatar', 'confirmed')

    def __init__(self, *args, **kwargs):
        self.position = kwargs.pop('position', None)
        super(PlayerSerializer, self).__init__(*args, **kwargs)

    def get_confirmed(self, obj):
        if self.position is None:
            return False

        # Hack Hack Hack
        team_attr = self.position + '_confirmed'
        rel = getattr(obj, self.position)
        return getattr(rel.first(), team_attr)

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ('pk', 'player', 'uuid')


class TeamSerializer(serializers.ModelSerializer):
    red_1 = PlayerSerializer(many=False, required=False, position='red_1')
    red_2 = PlayerSerializer(many=False, required=False, position='red_2')
    blue_1 = PlayerSerializer(many=False, required=False, position='blue_1')
    blue_2 = PlayerSerializer(many=False, required=False, position='blue_2')

    class Meta:
        model = Team
        fields = ('red_1', 'red_2', 'blue_1', 'blue_2', 'red_1_confirmed', 'red_2_confirmed', 'blue_1_confirmed',
                  'blue_2_confirmed')

class ProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(default='', required=False)

    class Meta:
        model = Player
        fields = ('pk', 'username', 'avatar', 'uuid')

    def create(self, validated_data):
        player, _ = Player.objects.get_or_create(username=validated_data["username"], avatar=validated_data["avatar"])
        mobile, _ = Mobile.objects.get_or_create(player=player, uuid=validated_data["uuid"])
        return player


class MatchSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    red_1 = serializers.IntegerField(write_only=True, required=False)
    red_2 = serializers.IntegerField(write_only=True, required=False)
    blue_1 = serializers.IntegerField(write_only=True, required=False)
    blue_2 = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Match
        fields = ('pk', 'team', 'goal_red', 'goal_blue', 'start', 'end', 'state', 'red_1', 'red_2', 'blue_1', 'blue_2')

    def update(self, instance, validated_data):
        if instance.state == Match.STATE_WAITING:
            allowed = ['red_1', 'red_2', 'blue_1', 'blue_2']
            team = instance.team

            for key, value in validated_data:
                if key in allowed and getattr(team, key, None) is None:
                    player = Player.objects.get(pk=value)
                    setattr(team, key, player)
                    setattr(team, key + "_confirmed", True)
                    team.save()
                    if team.all_confirmed():
                        instance.state = Match.STATE_ACTIVE
                        instance.save()
                    break
        return instance


class GoalSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    goal_date = serializers.CharField(read_only=True)

    class Meta:
        model = Goal
        fields = ('match', 'goal_date', 'side')

    def create(self, validated_data):
        match = get_object_or_404(Match, state=Match.STATE_ACTIVE)
        if validated_data["side"] == Goal.SIDE_RED:
            match.goal_red += 1
        else:
            match.goal_blue += 1
        match.save()
        goal, _ = Goal.objects.get_or_create(match=match, side=validated_data["side"])
        return goal
