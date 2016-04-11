from .models import Player, Mobile, Match, Team, Goal

from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('pk', 'username')


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ('pk', 'player', 'uuid')


class TeamSerializer(serializers.ModelSerializer):
    red_1 = PlayerSerializer(many=False, required=False)
    red_2 = PlayerSerializer(many=False, required=False)
    blue_1 = PlayerSerializer(many=False, required=False)
    blue_2 = PlayerSerializer(many=False, required=False)

    class Meta:
        model = Team
        fields = ('red_1', 'red_2', 'blue_1', 'blue_2')


class ProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(write_only=True)

    class Meta:
        model = Player
        fields = ('pk', 'username', 'uuid')

    def create(self, validated_data):
        player, _ = Player.objects.get_or_create(username=validated_data["username"])
        mobile, _ = Mobile.objects.get_or_create(player=player, uuid=validated_data["uuid"])
        return player


class MatchSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Match
        fields = ('team', 'goal_red', 'goal_blue', 'start', 'end', 'state')


class GoalSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    goal_date = serializers.CharField(read_only=True)

    class Meta:
        model = Goal
        fields = ('match', 'goal_date', 'side')
