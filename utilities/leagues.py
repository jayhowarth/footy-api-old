import json
from utilities.api_manager import APIManager as api
from utilities import mongo as mg
from datetime import datetime
from django.utils import timezone


def add_leagues():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    querystring = {}
    response = api.get_request(url, querystring)
    json_response = json.loads(response)
    total_countries = json_response['results']
    all_leagues = json_response['response']
    no_added = 0
    for x in all_leagues:
        league_id = x['league']['id']
        league_name = x['league']['name']
        league_type = x['league']['type']
        league_logo = x['league']['logo']
        league_country_name = x['country']['name']
        league_country_code = x['country']['code']
        league_country_flag = x['country']['flag']
        league_seasons = x['seasons']
        has_statistics = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['statistics_fixtures']
        has_events = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['events']
        has_lineups = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['lineups']
        has_player_stats = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['statistics_players']
        has_standings = x['seasons'][len(league_seasons) - 1]['coverage']['standings']
        has_players = x['seasons'][len(league_seasons) - 1]['coverage']['players']
        has_top_scorers = x['seasons'][len(league_seasons) - 1]['coverage']['top_scorers']
        has_top_assists = x['seasons'][len(league_seasons) - 1]['coverage']['top_assists']
        has_top_cards = x['seasons'][len(league_seasons) - 1]['coverage']['top_cards']
        has_injuries = x['seasons'][len(league_seasons) - 1]['coverage']['injuries']
        has_predictions = x['seasons'][len(league_seasons) - 1]['coverage']['predictions']
        has_odds = x['seasons'][len(league_seasons) - 1]['coverage']['odds']

        league = {
            "id": league_id,
            "name": league_name,
            "type": league_type,
            "logo": league_logo,
            "country_name": league_country_name,
            "country_code": league_country_code,
            "country_flag": league_country_flag,
            "league_seasons": league_seasons,
            "last_updated": datetime.utcnow(),
            "has_statistics": has_statistics,
            "has_events": has_events,
            "has_lineups": has_lineups,
            "has_player_stats": has_player_stats,
            "standings": has_standings,
            "players": has_players,
            "top_scorers": has_top_scorers,
            "top_assists": has_top_assists,
            "top_cards": has_top_cards,
            "injuries": has_injuries,
            "predictions": has_predictions,
            "odds": has_odds
        }
        count = mg.count_documents("leagues", {"id": league_id})
        if count == 0 or count is None:
            mg.add_record("leagues", league)
            no_added += 1

    return f'{no_added} Leagues'


def update_leagues():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    querystring = {}
    response = api.get_request(url, querystring)
    json_response = json.loads(response)
    total_countries = json_response['results']
    all_leagues = json_response['response']
    no_added = 0
    no_updated = 0
    for x in all_leagues:
        league_id = x['league']['id']
        league_name = x['league']['name']
        league_type = x['league']['type']
        league_logo = x['league']['logo']
        league_country_name = x['country']['name']
        league_country_code = x['country']['code']
        league_country_flag = x['country']['flag']
        league_seasons = x['seasons']
        has_statistics = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['statistics_fixtures']
        has_events = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['events']
        has_lineups = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['lineups']
        has_player_stats = x['seasons'][len(league_seasons) - 1]['coverage']['fixtures']['statistics_players']
        has_standings = x['seasons'][len(league_seasons) - 1]['coverage']['standings']
        has_players = x['seasons'][len(league_seasons) - 1]['coverage']['players']
        has_top_scorers = x['seasons'][len(league_seasons) - 1]['coverage']['top_scorers']
        has_top_assists = x['seasons'][len(league_seasons) - 1]['coverage']['top_assists']
        has_top_cards = x['seasons'][len(league_seasons) - 1]['coverage']['top_cards']
        has_injuries = x['seasons'][len(league_seasons) - 1]['coverage']['injuries']
        has_predictions = x['seasons'][len(league_seasons) - 1]['coverage']['predictions']
        has_odds = x['seasons'][len(league_seasons) - 1]['coverage']['odds']
        is_current = x['seasons'][len(league_seasons) - 1]['current']
        league = {
            "id": league_id,
            "name": league_name,
            "type": league_type,
            "logo": league_logo,
            "country_name": league_country_name,
            "country_code": league_country_code,
            "country_flag": league_country_flag,
            "league_seasons": league_seasons,
            "last_updated": datetime.utcnow(),
            "has_statistics": has_statistics,
            "has_events": has_events,
            "has_lineups": has_lineups,
            "has_player_stats": has_player_stats,
            "standings": has_standings,
            "players": has_players,
            "top_scorers": has_top_scorers,
            "top_assists": has_top_assists,
            "top_cards": has_top_cards,
            "injuries": has_injuries,
            "predictions": has_predictions,
            "odds": has_odds
        }
        count = mg.count_documents("leagues", {"id": league_id})
        if is_current:
            if count == 0 or count is None:
                mg.add_record("leagues", league)
                no_added += 1
            else:
                mg.update_record("leagues", {"id": league_id}, league)
                no_updated += 1

    return f'added {no_added} Leagues, updated {no_updated} leagues'


def get_league_and_country_by_id(league_id):
    league = mg.get_single_info("leagues", {"id": league_id})
    return league['name'], league['country_name']

def check_if_league(league_id):
    league = mg.get_single_info("leagues", {"id": league_id})
    if league['type'] == 'League':
        return True
    else:
        return False

def check_league_attributes(league_id):
    league = mg.get_single_info("leagues", {"id": league_id})
    try:
        attributes = {
            "has_events": league['has_events'],
            "has_lineups": league['has_lineups'],
            "has_player_stats": league['has_player_stats'],
            "has_statistics": league['has_statistics'],
            "has_injuries": league['injuries'],
            "has_odds": league['odds'],
            "has_players": league['players'],
            "has_predictions": league['predictions'],
            "has_standings": league['standings'],
            "has_assists": league['top_assists'],
            "has_cards": league['top_cards'],
            "has_scorers": league['top_scorers']
        }
    except TypeError:
        attributes = {
            "has_events": False,
            "has_lineups": False,
            "has_player_stats": False,
            "has_statistics": False,
            "has_injuries": False,
            "has_odds": False,
            "has_players": False,
            "has_predictions": False,
            "has_standings": False,
            "has_assists": False,
            "has_cards": False,
            "has_scorers": False
        }

    return attributes
