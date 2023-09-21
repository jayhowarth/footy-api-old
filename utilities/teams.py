import json
from datetime import datetime, timezone
from utilities.api_manager import APIManager as api
from utilities import mongo as mg

teams_url = "https://api-football-v1.p.rapidapi.com/v3/teams"
leagues_url = "https://api-football-v1.p.rapidapi.com/v3/leagues"


def update_all_teams_by_league():
    teams_updated = []
    all_leagues = mg.get_multiple_info("leagues")
    for x in all_leagues:
        added = update_teams_by_league(x['id'])
        if added:
            teams_updated.append({f"Leagues added {x['name']}"})
    if len(teams_updated) > 0:
        return teams_updated
    else:
        return "No teams added"


def update_all_teams_by_country():
    teams_updated = []
    all_countries = mg.get_multiple_info("countries")
    for x in all_countries:
        added = update_teams_by_country(x['name'])
        if added:
            teams_updated.append({f"Countries added {x['name']}"})
    if len(teams_updated) > 0:
        return teams_updated
    else:
        return "No teams added"


def update_teams_by_country(country_name):
    querystring = {"country": country_name}
    country_response = api.get_request(teams_url, querystring)
    json_response = json.loads(country_response)
    total = json_response['results']
    no_teams_added = 0
    teams = json_response['response']

    if total > 0:
        for x in teams:
            team_id = x["team"]["id"]
            team = {
                "id": team_id,
                "name": x["team"]["name"],
                "code": x["team"]["code"],
                "country": x["team"]["country"],
                "founded": x["team"]["founded"],
                "national": x["team"]["national"],
                "logo": x["team"]["logo"],
                "venue": x["venue"]
            }

            count = mg.count_documents("teams", {"id": team_id})
            if count == 0 or count is None:
                mg.add_record("teams", team)
                no_teams_added += 1

        return f'{no_teams_added} teams added'


def update_teams_by_league(league_id):
    current_season = datetime.today().strftime("%Y")
    querystring = {"league": league_id, "season": current_season}
    teams_response = api.get_request(teams_url, querystring)
    json_response = json.loads(teams_response)
    total = json_response['results']
    no_teams_added = 0
    teams = json_response['response']
    if total > 0:
        for x in teams:
            team_id = x["team"]["id"]
            team = {
                "id": team_id,
                "name": x["team"]["name"],
                "code": x["team"]["code"],
                "country": x["team"]["country"],
                "founded": x["team"]["founded"],
                "national": x["team"]["national"],
                "logo": x["team"]["logo"],
                "venue": x["venue"]
            }

            count = mg.count_documents("teams", {"id": team_id})
            if count == 0 or count is None:
                mg.add_record("teams", team)
                no_teams_added += 1

        return f'{no_teams_added} teams added'


def add_one_team(team_id):
    querystring = {"id": team_id}
    teams_response = api.get_request(teams_url, querystring)
    json_response = json.loads(teams_response)
    team_json = json_response['response'][0]
    team_id = team_json["team"]["id"]
    team = {
        "id": team_id,
        "name": team_json["team"]["name"],
        "code": team_json["team"]["code"],
        "country": team_json["team"]["country"],
        "founded": team_json["team"]["founded"],
        "national": team_json["team"]["national"],
        "logo": team_json["team"]["logo"],
        "venue": team_json["venue"]
    }

    count = mg.count_documents("teams", {"id": team_id})
    if count == 0 or count is None:
        mg.add_record("teams", team)
    else:
        mg.update_record("teams", {"id": team_id}, team)
    new_count = mg.count_documents("teams", {"id": team_id})
    return new_count


def check_when_last_team_fixtures_updated(team_id):
    team = mg.get_single_info("teams", {"id": team_id})
    try:
        last_updated = team['last_match_update']
        time_delta = datetime.utcnow() - last_updated
        if time_delta > timezone.timedelta(days=1):
            return True
        else:
            return False
    except KeyError:
        return True
    except TypeError:
        return True



