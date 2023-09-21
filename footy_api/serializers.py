from django.contrib.auth.models import User, Group
from footy_api import models
from rest_framework import serializers


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CompetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Competition
        fields = '__all__'


# class LeaguesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.League
#         fields = '__all__'


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'


class FederationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Federation
        fields = '__all__'


class LeagueStandingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeagueStandings
        fields = '__all__'
        # fields = ['season_id', 'name', 'rank', 'points', 'matches', 'last_updated']


class AllMatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AllMatches
        fields = '__all__'


class PlayerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayerEvent
        fields = '__all__'
