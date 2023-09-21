import requests
from django.utils import timezone
from datetime import timedelta
#from acca_api.views import GetLeagueStandingsViewset
from footy_api.models import LeagueStandings, Competition
from footy_api.serializers import LeagueStandingsSerializer
from footy import config

league_table_url = "http://livescore-api.com/api-client/leagues/table.json"
league_list_url = "http://livescore-api.com/api-client/leagues/list.json"


# def update_leagues():
#     live_scores_url = league_list_url + "?" + config.live_scores_auth
#     response = requests.get(live_scores_url)
#     json_response = response.json()
#     total = len(json_response['data']['league'])
#     no_added = 0
#     for x in range(0, total):
#         league_id = json_response['data']['league'][x]['id']
#         league_name = json_response['data']['league'][x]['name']
#         country_id = json_response['data']['league'][x]['country_id']
#         country = Country.objects.get(id=country_id)
#         league_live_score_url = json_response['data']['league'][x]['scores']
#
#         exists = League.objects.filter(id=league_id).exists()
#
#         if not exists:
#             leagues = League(id=league_id,
#                              name=league_name,
#                              country=country,
#                              live_score_url=league_live_score_url)
#
#             leagues.save()
#             no_added += 1
#
#     return f'{no_added} Leagues'

def update_all_league_tables():
    comps = Competition.objects.all().values()
    all_comps = [x for x in comps if x["federation_id"] is None]
    for y in all_comps:
        league = LeagueStandings.objects.filter(competition_id=y['id'])
        exists = league.exists()
        if not exists:
            try:
                add_league_standings(y['id'])
            except KeyError:
                print('key error')
        else:
            try:
                update_league_standings(y['id'])
            except KeyError:
                print('key error')

    return f'updated {len(all_comps)} leagues'


def add_league_standings(comp_id):
    live_scores_url = league_table_url + "?" + config.live_scores_auth
    response = requests.get(live_scores_url, params={"competition_id": str(comp_id)})
    json_response = response.json()
    total = len(json_response['data']['table'])
    league_name = competitions.get_competition_name(comp_id)
    league_table_size = len(json_response['data']['table'])
    if league_table_size > 0:
        for x in range(0, total):
            league_id = json_response['data']['table'][x]['league_id']
            season_id = json_response['data']['table'][x]['season_id']
            name = json_response['data']['table'][x]['name']
            rank = json_response['data']['table'][x]['rank']
            points = json_response['data']['table'][x]['points']
            matches = json_response['data']['table'][x]['matches']
            goal_diff = json_response['data']['table'][x]['goal_diff']
            goals_scored = json_response['data']['table'][x]['goals_scored']
            goals_conceded = json_response['data']['table'][x]['goals_conceded']
            lost = json_response['data']['table'][x]['lost']
            drawn = json_response['data']['table'][x]['drawn']
            won = json_response['data']['table'][x]['won']
            team_id = json_response['data']['table'][x]['team_id']
            competition_id = json_response['data']['table'][x]['competition_id']

            standings = LeagueStandings(league_id=league_id,
                                        season_id=season_id,
                                        name=name,
                                        rank=rank,
                                        points=points,
                                        matches=matches,
                                        goal_diff=goal_diff,
                                        goals_scored=goals_scored,
                                        goals_conceded=goals_conceded,
                                        lost=lost,
                                        drawn=drawn,
                                        won=won,
                                        team_id=team_id,
                                        competition_id=competition_id)
            standings.save()
        return f'Added {league_name}'


def update_league_standings(comp_id):
    last_updated = LeagueStandings.objects.filter(competition_id=comp_id).values('name', 'last_updated')
    league_name = competitions.get_competition_name(comp_id)
    time_delta = timezone.now() - last_updated[0]['last_updated']
    if time_delta > timezone.timedelta(hours=12):
        live_scores_url = league_table_url + "?" + config.live_scores_auth
        response = requests.get(live_scores_url, params={"competition_id": str(comp_id)})
        json_response = response.json()
        total = len(json_response['data']['table'])
        LeagueStandings.objects.filter(competition_id=comp_id).delete()
        for x in range(0, total):
            league_id = json_response['data']['table'][x]['league_id']
            season_id = json_response['data']['table'][x]['season_id']
            name = json_response['data']['table'][x]['name']
            rank = json_response['data']['table'][x]['rank']
            points = json_response['data']['table'][x]['points']
            matches = json_response['data']['table'][x]['matches']
            goal_diff = json_response['data']['table'][x]['goal_diff']
            goals_scored = json_response['data']['table'][x]['goals_scored']
            goals_conceded = json_response['data']['table'][x]['goals_conceded']
            lost = json_response['data']['table'][x]['lost']
            drawn = json_response['data']['table'][x]['drawn']
            won = json_response['data']['table'][x]['won']
            team_id = json_response['data']['table'][x]['team_id']
            competition_id = json_response['data']['table'][x]['competition_id']

            standings = LeagueStandings(league_id=league_id,
                                        season_id=season_id,
                                        name=name,
                                        rank=rank,
                                        points=points,
                                        matches=matches,
                                        goal_diff=goal_diff,
                                        goals_scored=goals_scored,
                                        goals_conceded=goals_conceded,
                                        lost=lost,
                                        drawn=drawn,
                                        won=won,
                                        team_id=team_id,
                                        competition_id=competition_id)
            standings.save()
        return f'Updated {league_name}'
    else:
        return f'Not updated {league_name}'


def check_league_standing(comp_id):
    league = LeagueStandings.objects.filter(competition_id=str(comp_id))
    if not league.exists():
        resp = add_league_standings(comp_id)
        return resp
    else:  
        val = league.values()
        date_updated = val[0]['last_updated']
        serializer = LeagueStandingsSerializer(league, many=True)
        #date_updated = serializer.data[0]['last_updated']
        one_day_ago = timezone.now() - timedelta(days=1)
        x = date_updated.strftime("%Y-%m-%d %H:%M")
        y = one_day_ago.strftime("%Y-%m-%d %H:%M")
        over_24_hours = one_day_ago > date_updated
        if over_24_hours:
            resp = update_league_standings(comp_id)
            return resp
        else:
            return 'No update needed'
         



