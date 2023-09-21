from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from dateutil import parser
from footy_api import models, serializers
from rest_framework import viewsets
from utilities import countries, \
    teams, \
    previous_fixtures, \
    fixtures, \
    leagues, \
    manual_db_add, \
    results, \
    league_standings, \
    score

from utilities import player_stats, statistics
from utilities.league_standings import update_league_standings_by_league
from .tasks import update_all_previous_matches_for_league, \
    update_previous_matches,    \
    update_all_previous_matches_for_selected_leagues, \
    update_selected_league_tables,  \
    update_h2h_for_todays_matches


class GetCountriesViewset(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountriesSerializer


class GetCompetitionsViewset(viewsets.ModelViewSet):
    queryset = models.Competition.objects.all()
    serializer_class = serializers.CompetitionsSerializer


# class GetLeaguesViewset(viewsets.ModelViewSet):
#     queryset = models.League.objects.all()
#     serializer_class = serializers.LeaguesSerializer


class GetTeamsViewset(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamsSerializer


class GetFederationsViewset(viewsets.ModelViewSet):
    queryset = models.Federation.objects.all()
    serializer_class = serializers.FederationsSerializer


class GetLeagueStandingsViewset(viewsets.ModelViewSet):
    queryset = models.LeagueStandings.objects.all()
    serializer_class = serializers.LeagueStandingsSerializer


class GetAllMatchesViewset(viewsets.ModelViewSet):
    queryset = models.AllMatches.objects.all()
    serializer_class = serializers.AllMatchesSerializer


class GetPlayerEventViewset(viewsets.ModelViewSet):
    queryset = models.PlayerEvent.objects.all()
    serializer_class = serializers.PlayerEventSerializer


def main_update(request):
    # fed_resp = federations.update_federations()
    country_resp = countries.update_countries()
    # leagues_resp = leagues.update_leagues()
    # comp_resp = competitions.update_competitions()
    # teams_resp = teams.update_teams()
    # response = f'Added {fed_resp}, {country_resp}, {comp_resp}, {teams_resp}'
    return HttpResponse(response)


# def get_competitions(request):
#     resp = competitions.update_competitions()
#     return HttpResponse(resp)


def get_countries(request):
    resp = countries.update_countries()
    return HttpResponse(resp)


def get_leagues(request):
    resp = leagues.update_leagues()
    return HttpResponse(resp)


# def get_federations(request):
#     resp = federations.update_federations()
#     return HttpResponse(resp)


def get_teams(request):
    resp = teams.update_all_teams_by_country()
    return HttpResponse(resp)


def get_matches(request, team_id):
    resp = previous_fixtures.add_matches(team_id)
    return HttpResponse(f'Added {resp[0]} matches for {resp[1]}')


# def get_standings(request, competition_id):
#     resp = competitions.check_league_standing(competition_id)
#     return HttpResponse(resp)


def get_all_standings(request):
    league_id = request.GET['league_id']
    resp = league_standings.all_teams_in_league(int(league_id))
    return HttpResponse(resp)

def update_league_standings(request):
    update_selected_league_tables.delay()
    return HttpResponse('Started Update Selected League Standings')
@csrf_exempt
def get_todays_fixtures(request):
    resp = fixtures.get_todays_fixtures()
    return JsonResponse(resp, safe=False)

@csrf_exempt
def get_fixtures_by_date(request):
    body = json.loads(request.body)
    selected_date = body['stuff']['date']
    resp = fixtures.get_fixtures_by_date(selected_date, False)
    return JsonResponse(resp, safe=False)


@csrf_exempt
def get_results_by_date(request):
    body = json.loads(request.body)
    selected_date = body['stuff']['date']
    resp = results.get_results_by_date(selected_date, False)
    return JsonResponse(resp, safe=False)

def update_todays_fixtures(request):
    update_previous_matches.delay()
    #update_all_previous_matches_for_selected_leagues.delay()
    return HttpResponse('Started Update of Today\'s Fixtures')

def update_fixtures_by_date(request):
    # update_previous_matches.delay()
    update_all_previous_matches_for_selected_leagues.delay()
    return HttpResponse('Started Update of Today\'s Fixtures')
    # return JsonResponse(resp, safe=False)


def update_all_fixtures_for_league(request):
    league_id = request.GET['league_id']
    update_all_previous_matches_for_league.delay(int(league_id))
    league, country = leagues.get_league_and_country_by_id(int(league_id))
    return HttpResponse(f'Started Update of Fixtures for {league}({country})')


def get_tomorrows_fixtures(request):
    resp = fixtures.get_tomorrows_fixtures()
    return JsonResponse(resp, safe=False)


def get_team_statistics(request, team_id):
    resp = team_statistics.get_over_1_5_goals(team_id)
    return JsonResponse(resp, safe=False)


def add_manually(request):
    resp = manual_db_add.add_team()
    return HttpResponse(resp)

@csrf_exempt
def test(request):
    # d = json.loads(request.body)
    # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # querystring = {"date": "2022-09-01"}
    # e = calc_team_statistics.get_league_stats(39,35)
    # home_id = request.GET['home_id']
    # away_id = request.GET['away_id']
    # fixture_id = request.GET['fixture_id']
    # e = statistics.get_players_with_most_yellow_cards(int(home_id))
    # f = statistics.get_players_with_most_yellow_cards(int(away_id))
    # e = statistics.get_players_with_most_cards(33)
    #f = statistics.get_all_h2h(45, 33)
    #t = statistics.get_last_x_away_matches(33, 3)
    # x = update_league_standings_by_league(87)
    # update_h2h_for_todays_matches.delay()
    # x = {'s': 'started'}
    # x = score.calculate_match_result_score(33, 45)
    #x = statistics.return_combined_team_stats('111111', 33, 45)
    #e = statistics.get_players_with_most_yellow_cards(32)
    # e=player_stats.update_all_players_in_squad(45)

    return JsonResponse("test", safe=False)


def dummy(request):
    stuff = [{
                "fixture_id": 964060,
                "fixture_status": "NS",
                "league_id": 525,
                "league_name": "UEFA Champions League Women",
                "league_country": "World",
                "league_logo": "https://media-1.api-sports.io/football/leagues/525.png",
                "league_flag": None,
                "fixture_time": "20:00:00",
                "fixture_date": "2022-12-22",
                # "fixture_date": "22-12-2022",
                "round": "Group Stage - 6",
                "location": "Estadio Alfredo Di Stéfano, Madrid",
                "home_name": "Real Madrid W",
                "home_id": 15224,
                "home_logo": "https://media.api-sports.io/football/teams/15224.png",
                "away_name": "Vllaznia",
                "away_id": 10906,
                "away_logo": "https://media.api-sports.io/football/teams/10906.png"
            },
            {
                "fixture_id": 964061,
                "fixture_status": "NS",
                "league_id": 525,
                "league_name": "UEFA Champions League Women",
                "league_country": "World",
                "league_logo": "https://media-1.api-sports.io/football/leagues/525.png",
                "league_flag": None,
                "fixture_time": "20:00:00",
                # "fixture_date": "22-12-2022",
                "fixture_date": "2023-01-03",
                "round": "Group Stage - 6",
                "location": "Stamford Bridge, London",
                "home_name": "Chelsea W",
                "home_id": 1853,
                "home_logo": "https://media.api-sports.io/football/teams/1853.png",
                "away_name": "Paris Saint Germain W",
                "away_id": 1667,
                "away_logo": "https://media.api-sports.io/football/teams/1667.png"
            },
            {
                "fixture_id": 969905,
                "fixture_status": "NS",
                "league_id": 392,
                "league_name": "Challenge League",
                "league_country": "Malta",
                "league_logo": "https://media.api-sports.io/football/leagues/392.png",
                "league_flag": "https://media-1.api-sports.io/flags/mt.svg",
                "fixture_time": "20:00:00",
                # "fixture_date": "22-12-2022",
                "fixture_date": "2022-12-22",
                "round": "1st Phase - 16",
                "location": "MFA Centenary Stadium, Ta'Qali",
                "home_name": "Mqabba",
                "home_id": 4604,
                "home_logo": "https://media-1.api-sports.io/football/teams/4604.png",
                "away_name": "Marsaskala",
                "away_id": 18269,
                "away_logo": "https://media-2.api-sports.io/football/teams/18269.png"
            },
            {
                "fixture_id": 969906,
                "fixture_status": "NS",
                "league_id": 392,
                "league_name": "Challenge League",
                "league_country": "Malta",
                "league_logo": "https://media.api-sports.io/football/leagues/392.png",
                "league_flag": "https://media-1.api-sports.io/flags/mt.svg",
                "fixture_time": "20:00:00",
                # "fixture_date": "22-12-2022",
                "fixture_date": "2023-01-04",
                "round": "1st Phase - 16",
                "location": "Victor Tedesco Stadium, Hamrun",
                "home_name": "Zejtun Corinthians",
                "home_id": 4615,
                "home_logo": "https://media.api-sports.io/football/teams/4615.png",
                "away_name": "Mtarfa",
                "away_id": 19696,
                "away_logo": "https://media-1.api-sports.io/football/teams/19696.png"
            },
            {
                "fixture_id": 972362,
                "fixture_status": "NS",
                "league_id": 48,
                "league_name": "League Cup",
                "league_country": "England",
                "league_logo": "https://media.api-sports.io/football/leagues/48.png",
                "league_flag": "https://media.api-sports.io/flags/gb.svg",
                "fixture_time": "20:00:00",
                # "fixture_date": "22-12-2022",
                "fixture_date": "2022-12-22",
                "round": "Round of 16",
                "location": "Etihad Stadium, Manchester",
                "home_name": "Manchester City",
                "home_id": 50,
                "home_logo": "https://media.api-sports.io/football/teams/50.png",
                "away_name": "Liverpool",
                "away_id": 40,
                "away_logo": "https://media-1.api-sports.io/football/teams/40.png"
            }]
    return JsonResponse(stuff, safe=False)

def stats(request):
    stats = player_stats.update_all_players_in_league(48)
    return JsonResponse(stats, safe=False)