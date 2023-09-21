import json

from django.utils.dateparse import parse_datetime
from datetime import datetime, timezone, timedelta
import asyncio
from utilities.teams import check_when_last_team_fixtures_updated, add_one_team
from utilities.api_manager import APIManager as api
from utilities import mongo as mg
from utilities.fixtures import get_todays_fixtures, get_tomorrows_fixtures
from footy_api.tasks import update_previous_matches
from utilities import update_validator

matches_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"


# def update_previous_matches_for_todays_fixtures():
#     fixtures = get_todays_fixtures()
#     total_added = 0
#     home_added = 0
#     away_added = 0
#     h2h_added = 0
#     for idx, x in enumerate(fixtures):
#         # home_updated = check_when_last_team_fixtures_updated(x['home_id'])
#         # away_updated = check_when_last_team_fixtures_updated(x['away_id'])
#         # if home_updated:
#         #     home = add_previous_matches(x['home_id'])
#         #     home_added = home[0]
#         # if away_updated:
#         #     away = add_previous_matches(x['away_id'])
#         #     away_added = away[0]
#         # if home_updated and away_updated:
#         #     h2h_added = get_h2h_matches(x['home_id'], x['away_id'])
#         print(idx)
#         update_previous_matches.delay(x)
#     return total_added

def update_previous_matches_in_league(league_id):
    fixtures = get_todays_fixtures()
    total_added = 0
    for x in fixtures:
        if x['league_id'] == league_id:
            home_added = add_previous_matches(x['home_id'])
            away_added = add_previous_matches(x['away_id'])
            h2h_added = get_h2h_matches(x['home_id'], x['away_id'])
            total_added += (home_added[0] + away_added[0] + h2h_added)
    return total_added


def update_previous_matches_for_todays_fixtures_in_league(league_id):
    fixtures = get_todays_fixtures()
    total_added = 0
    for x in fixtures:
        if x['league_id'] == league_id:
            home_added = add_previous_matches(x['home_id'])
            away_added = add_previous_matches(x['away_id'])
            h2h_added = get_h2h_matches(x['home_id'], x['away_id'])
            total_added += (home_added[0] + away_added[0] + h2h_added)
    return total_added


def add_previous_matches_by_league(league_id):
    league = mg.get_single_info("standings", {"id": league_id})
    league_teams = league['standings']
    all_added = []
    for x in league_teams:
        resp = update_teams_previous_matches(x['team']['id'], 20)
        team_name = mg.get_single_info("teams", {"id": x['team']['id']})
        all_added.append({resp, team_name['name']})
    return all_added


def add_previous_matches(team_id):
    resp = update_teams_previous_matches(team_id, 20)
    try:
        team_name = mg.get_single_info("teams", {"id": team_id})
        return resp, team_name['name']
    except TypeError:
        new_team = add_one_team(team_id)
        team_name = {}
        while new_team < 1:
            team_name = mg.get_single_info("teams", {"id": team_id})
            new_team = mg.count_documents("teams", {"id": team_id})
        return resp, team_name
    except KeyError:
        new_team = add_one_team(team_id)
        while new_team < 1:
            new_team = mg.count_documents("teams", {"id": team_id})
        team_name = mg.get_single_info("teams", {"id": team_id})
        return resp, team_name['name']


def update_teams_previous_matches(team_id, num_matches):
    querystring = {"team": team_id, "last": num_matches}
    fixture_response = api.get_request(matches_url, querystring)
    if fixture_response is not '':
        try:
            json_response = json.loads(fixture_response)
            total = json_response['results']
            fixtures = json_response['response']
        except TypeError:
            print('Error in fixture response')
            fixtures = None
            total = 0
    else:
        total = 0
        fixtures = []
    no_matches_added = 0
    if total > 0:
        for x in fixtures:
            if x['fixture']['status']['short'] == "FT":
                fixture_id = x['fixture']['id']
                league_id = x['league']['id']
                if not mg.document_exists("fixtures", {"id": fixture_id}):
                    home_stats, away_stats = get_fixture_statistics(fixture_id, league_id)
                    fixture = {
                        "id": fixture_id,
                        "date": x['fixture']['date'],
                        "timestamp": x['fixture']['timestamp'],
                        "venue": x['fixture']['venue'],
                        "league_id": league_id,
                        "league_name": x['league']['name'],
                        "league_country": x['league']['country'],
                        "league_logo": x['league']['logo'],
                        "league_flag": x['league']['flag'],
                        "league_season": x['league']['season'],
                        "league_round": x['league']['round'],
                        "home_id": x['teams']['home']['id'],
                        "home_name": x['teams']['home']['name'],
                        "home_logo": x['teams']['home']['logo'],
                        "away_id": x['teams']['away']['id'],
                        "away_name": x['teams']['away']['name'],
                        "away_logo": x['teams']['away']['logo'],
                        "goals_home": x['goals']['home'],
                        "goals_away": x['goals']['away'],
                        "score": x['score'],
                        "events": get_fixture_events(fixture_id, league_id),
                        "statistics_home": home_stats,
                        "statistics_away": away_stats,
                    }
                    mg.add_record("fixtures", fixture)
                    no_matches_added += 1
        # last_fix_status = fixtures[0]['fixture']['status']['short']
        # last_fix_date = fixtures[0]['fixture']['date']
        # last_fix_id = fixtures[0]['fixture']['id']
        mg.update_one_record("teams", {"id": team_id}, {"$set": {"last_match_update": datetime.utcnow()}})
        return no_matches_added
    else:
        return 0


def update_fixtures_by_id(fixture_ids):
    query = f"{fixture_ids[0]}"
    if len(fixture_ids) > 1:
        for x in range(1, len(fixture_ids)):
            if x <= 20:
                query = query+"-"+str(fixture_ids[x])
    querystring = {"ids": query}
    fixture_response = api.get_request(matches_url, querystring)
    json_response = json.loads(fixture_response)
    fixtures = json_response['response']
    no_matches_added = 0
    for x in fixtures:
        fixture_id = x['fixture']['id']
        league_id = x['league']['id']
        if not mg.document_exists("fixtures", {"id": fixture_id}):
            home_stats, away_stats = get_fixture_statistics(fixture_id, league_id)
            fixture = {
                "id": fixture_id,
                "date": x['fixture']['date'],
                "timestamp": x['fixture']['timestamp'],
                "venue": x['fixture']['venue'],
                "league_id": league_id,
                "league_name": x['league']['name'],
                "league_country": x['league']['country'],
                "league_logo": x['league']['logo'],
                "league_flag": x['league']['flag'],
                "league_season": x['league']['season'],
                "league_round": x['league']['round'],
                "home_id": x['teams']['home']['id'],
                "home_name": x['teams']['home']['name'],
                "home_logo": x['teams']['home']['logo'],
                "away_id": x['teams']['away']['id'],
                "away_name": x['teams']['away']['name'],
                "away_logo": x['teams']['away']['logo'],
                "goals_home": x['goals']['home'],
                "goals_away": x['goals']['away'],
                "score": x['score'],
                "events": get_fixture_events(fixture_id, league_id),
                "statistics_home": home_stats,
                "statistics_away": away_stats,
            }
            mg.add_record("fixtures", fixture)
            no_matches_added += 1
    return no_matches_added


def get_fixture_events(fixture_id, league_id):
    querystring = {"fixture": fixture_id}
    if check_if_league_has_events(league_id):
        event_response = api.get_request(matches_url+"/events", querystring)
        json_response = json.loads(event_response)
        total = json_response['results']

        if total > 0:
            return json_response['response']
        else:
            return None
    else:
        return None


def create_statistics_json(stat_array):
    fixture_json = {}
    for x in stat_array:
        fixture_json.update({x['type']: x['value']})
    return fixture_json


def get_fixture_statistics(fixture_id, league_id):
    if check_if_league_has_statistics(league_id):
        querystring = {"fixture": fixture_id}
        stat_response = api.get_request(matches_url + "/statistics", querystring)
        json_response = json.loads(stat_response)
        total = json_response['results']
        if total > 0 and len(json_response['response'][0]) > 0:
            home_fixture_stats = json_response['response'][0]
            home_team_stats = {
                "team_id": home_fixture_stats['team']['id'],
                "team_name": home_fixture_stats['team']['name'],
                "statistics": create_statistics_json(home_fixture_stats['statistics'])
            }
        else:
            home_team_stats = {}

        if total > 0 and len(json_response['response'][1]) > 0:
            away_fixture_stats = json_response['response'][1]
            away_team_stats = {
                "team_id": away_fixture_stats['team']['id'],
                "team_name": away_fixture_stats['team']['name'],
                "statistics": create_statistics_json(away_fixture_stats['statistics'])
            }
        else:
            away_team_stats = {}
    else:
        home_team_stats = {}
        away_team_stats = {}

    return home_team_stats, away_team_stats


def get_h2h_matches(home_team_id, away_team_id):
    querystring = {"h2h": f"{home_team_id}-{away_team_id}", "status": "FT"}
    h2h_response = api.get_request(matches_url + "/headtohead", querystring)
    response = json.loads(h2h_response)
    no_matches_added = 0
    fixtures = response['response']
    for x in fixtures:
        fixture_id = x['fixture']['id']
        league_id = x['league']['id']
        if not mg.document_exists("fixtures", {"id": fixture_id}):
            home_stats, away_stats = get_fixture_statistics(fixture_id, league_id)
            fixture = {
                "id": fixture_id,
                "date": x['fixture']['date'],
                "timestamp": x['fixture']['timestamp'],
                "venue": x['fixture']['venue'],
                "league_id": league_id,
                "league_name": x['league']['name'],
                "league_country": x['league']['country'],
                "league_logo": x['league']['logo'],
                "league_flag": x['league']['flag'],
                "league_season": x['league']['season'],
                "league_round": x['league']['round'],
                "home_id": x['teams']['home']['id'],
                "home_name": x['teams']['home']['name'],
                "home_logo": x['teams']['home']['logo'],
                "away_id": x['teams']['away']['id'],
                "away_name": x['teams']['away']['name'],
                "away_logo": x['teams']['away']['logo'],
                "goals_home": x['goals']['home'],
                "goals_away": x['goals']['away'],
                "score": x['score'],
                "events": get_fixture_events(fixture_id, league_id),
                "statistics_home": home_stats,
                "statistics_away": away_stats,
            }
            mg.add_record("fixtures", fixture)
            no_matches_added += 1
    return no_matches_added


def check_if_league_has_statistics(league_id):
    league = mg.get_single_info("leagues", {"id": league_id})
    try:
        return league['has_statistics']
    except KeyError:
        return True
    except TypeError:
        return True


def check_if_league_has_events(league_id):
    league = mg.get_single_info("leagues", {"id": league_id})
    try:
        return league['has_events']
    except KeyError:
        return True
    except TypeError:
        return True
