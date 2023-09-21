import json
from datetime import datetime, timezone
from django.utils import timezone
from utilities.api_manager import APIManager as api
from utilities import mongo as mg

league_table_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
current_season = datetime.today().strftime("%Y")


def update_all_league_tables():
    leagues_updated = []
    all_leagues = mg.get_multiple_info("leagues")
    added = False
    for x in all_leagues:
        check = check_current_season_and_standings(x)
        if check["standings"] is True and check["is_current"] is True:
            added = update_league_standings_by_league(x['id'])
        if added:
            leagues_updated.append({"League": x['name'], "Country": x['country_name']})
    if len(leagues_updated) > 0:
        return leagues_updated
    else:
        return "No teams added"


def update_league_standings_by_league(league_id):
    league_updated = False
    count = mg.count_documents("standings", {"id": league_id})
    time_delta = mg.check_last_updated("standings", {"id": league_id})
    if time_delta > timezone.timedelta(hours=12) or count == 0 or count is None:
        querystring = {"league": league_id, "season": current_season}
        standings_response = api.get_request(league_table_url, querystring)
        json_response = json.loads(standings_response)
        total = json_response['results']
        standings = json_response['response']

        if total > 0:
            for x in standings:
                standings_id = x["league"]["id"]
                all_standings = {
                    "id": standings_id,
                    "name": x["league"]["name"],
                    "country": x["league"]["country"],
                    "logo": x["league"]["logo"],
                    "flag": x["league"]["flag"],
                    "season": x["league"]["season"],
                    "standings": x["league"]["standings"][0],
                    "last_updated": datetime.utcnow()
                    }
                if count == 0:
                    mg.add_record("standings", all_standings)
                    league_updated = True
                else:
                    mg.update_record("standings", {"id": standings_id}, all_standings)
                    league_updated = True
        else:
            league_updated = False
        return league_updated
    else:
        return league_updated


def all_teams_in_league(league_id):
    count = mg.count_documents("standings", {"id": league_id})
    time_delta = mg.check_last_updated("standings", {"id": league_id})
    if time_delta > timezone.timedelta(hours=12) or count == 0 or count is None:
        update_league_standings_by_league(league_id)
    league = mg.get_single_info("standings", {"id": league_id})
    standings = league['standings']
    return standings


def check_current_season_and_standings(data):
    has_standings = False
    is_current = False
    for x in data["league_seasons"]:
        if x["current"] is True:
            is_current = True
            if x["coverage"]["standings"] is True:
                has_standings = True
    return {"standings": has_standings, "is_current": is_current}



# def update_league_standings(comp_id):
#     last_updated = LeagueStandings.objects.filter(competition_id=comp_id).values('name', 'last_updated')
#     league_name = competitions.get_competition_name(comp_id)
#     time_delta = timezone.now() - last_updated[0]['last_updated']
#     if time_delta > timezone.timedelta(hours=12):
#         live_scores_url = league_table_url + "?" + config.live_scores_auth
#         response = requests.get(live_scores_url, params={"competition_id": str(comp_id)})
#         json_response = response.json()
#         total = len(json_response['data']['table'])
#         LeagueStandings.objects.filter(competition_id=comp_id).delete()
#         for x in range(0, total):
#             league_id = json_response['data']['table'][x]['league_id']
#             season_id = json_response['data']['table'][x]['season_id']
#             name = json_response['data']['table'][x]['name']
#             rank = json_response['data']['table'][x]['rank']
#             points = json_response['data']['table'][x]['points']
#             matches = json_response['data']['table'][x]['matches']
#             goal_diff = json_response['data']['table'][x]['goal_diff']
#             goals_scored = json_response['data']['table'][x]['goals_scored']
#             goals_conceded = json_response['data']['table'][x]['goals_conceded']
#             lost = json_response['data']['table'][x]['lost']
#             drawn = json_response['data']['table'][x]['drawn']
#             won = json_response['data']['table'][x]['won']
#             team_id = json_response['data']['table'][x]['team_id']
#             competition_id = json_response['data']['table'][x]['competition_id']
#
#             standings = LeagueStandings(league_id=league_id,
#                                         season_id=season_id,
#                                         name=name,
#                                         rank=rank,
#                                         points=points,
#                                         matches=matches,
#                                         goal_diff=goal_diff,
#                                         goals_scored=goals_scored,
#                                         goals_conceded=goals_conceded,
#                                         lost=lost,
#                                         drawn=drawn,
#                                         won=won,
#                                         team_id=team_id,
#                                         competition_id=competition_id)
#             standings.save()
#         return f'Updated {league_name}'
#     else:
#         return f'Not updated {league_name}'
#
#
# def check_league_standing(comp_id):
#     league = LeagueStandings.objects.filter(competition_id=str(comp_id))
#     if not league.exists():
#         resp = add_league_standings(comp_id)
#         return resp
#     else:
#         val = league.values()
#         date_updated = val[0]['last_updated']
#         serializer = LeagueStandingsSerializer(league, many=True)
#         #date_updated = serializer.data[0]['last_updated']
#         one_day_ago = timezone.now() - timedelta(days=1)
#         x = date_updated.strftime("%Y-%m-%d %H:%M")
#         y = one_day_ago.strftime("%Y-%m-%d %H:%M")
#         over_24_hours = one_day_ago > date_updated
#         if over_24_hours:
#             resp = update_league_standings(comp_id)
#             return resp
#         else:
#             return 'No update needed'
         



