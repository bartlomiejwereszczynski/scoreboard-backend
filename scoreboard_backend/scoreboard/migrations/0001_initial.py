# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 10:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_red', models.IntegerField(default=0)),
                ('goal_blue', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blue_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blue_1', to='scoreboard.Player')),
                ('blue_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blue_2', to='scoreboard.Player')),
                ('red_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='red_1', to='scoreboard.Player')),
                ('red_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='red_2', to='scoreboard.Player')),
            ],
        ),
        migrations.AddField(
            model_name='mobile',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.Team'),
        ),
        migrations.AddField(
            model_name='goal',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.Match'),
        ),
    ]