from __future__ import unicode_literals

from django.db import models

SIDE_BLUE = 'blue'
SIDE_RED = 'red'

SIDES = (
    (SIDE_BLUE, 'Blue'),
    (SIDE_RED, 'Red'),
)


# Create your models here.
class Player(models.Model):
    username = models.CharField(max_length=200)

    def __unicode__(self):
        return self.username


class Mobile(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200)

    def __unicode__(self):
        return self.uuid


class Team(models.Model):
    red_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="red_1", blank=True, null=True)
    red_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="red_2", blank=True, null=True)
    blue_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="blue_1", blank=True, null=True)
    blue_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="blue_2", blank=True, null=True)

    def __unicode__(self):
        return "Red: {}, {}; Blue: {}, {}".format(self.red_1, self.red_2, self.blue_1, self.blue_2)


class Match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal_red = models.IntegerField(default=0)
    goal_blue = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return


class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    goal_date = models.DateTimeField(auto_now_add=True)
    side = models.CharField(max_length=5, choices=SIDES)
