from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Player, Mobile, Match, Team, Goal


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

    def save(self, **kwargs):
        if self.instance is None:
            return super(MatchSerializer, self).save(**kwargs)

        if self.instance.state != Match.STATE_WAITING:
            return self.instance

        allowed = {'red_1', 'red_2', 'blue_1', 'blue_2'}
        team = self.instance.team

        for key, value in self.validated_data.iteritems():
            if key not in allowed:
                continue

            if value == 0:
                player = None
                confirmed = False
            elif team.player_present(value):
                continue
            else:
                player = get_object_or_404(Player, pk=value)
                confirmed = True

            setattr(team, key, player)
            setattr(team, key + "_confirmed", confirmed)
            team.save()

            if team.all_confirmed():
                self.instance.state = Match.STATE_ACTIVE
            else:
                self.instance.state = Match.STATE_WAITING

            self.instance.save()

            break

        return self.instance


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


KNOWN_ROLES = ('red_1', 'red_2', 'blue_1', 'blue_2')


class ConfirmSerializer(serializers.Serializer):
    role = serializers.CharField()
    action = serializers.CharField()

    def validate_role(self, role):
        if role not in KNOWN_ROLES:
            raise ValidationError('Unknown role "{}"'.format(role))

        return role

    def validate_action(self, action):
        if action not in ('accept', 'reject'):
            raise ValidationError('Unknown action "{}"'.format(action))

        return action

    def save(self, **kwargs):
        role = self.validated_data['role']
        confirm = True if self.validated_data['action'] == 'accept' else False

        match = kwargs.pop('match')
        team = match.team

        if not confirm:
            # You can't quit a match
            if match.state != Match.STATE_WAITING:
                return match

            setattr(team, role, None)
            setattr(team, role + '_confirmed', False)
            match.state = Match.STATE_WAITING
        else:
            setattr(team, role + '_confirmed', True)

        if team.all_confirmed():
            match.state = Match.STATE_ACTIVE

        team.save()
        match.save()