import json

from dateutil import parser

from utilities.api_manager import APIManager as api
from django.utils import timezone
import datetime
from datetime import datetime, date, timedelta
from utilities import mongo as mg
from utilities import leagues

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
league_list = [39, 40, 41, 42, 43, 45, 48,
        135, 136, 137, 140, 141, 143, 61, 62, 66, 88,
        89, 78, 79, 80, 94, 97,
        103, 104, 113, 114, 115, 119, 120, 144, 145, 147, 179,
        180, 181, 182, 183, 184, 185, 207, 208, 218, 219 ]


def get_results_by_date(fixture_date, filter_league):
    converted_date = parser.parse(fixture_date)
    filtered_date = converted_date.strftime('%Y-%m-%d')
    if filter_league:
        filter_league = league_list
    else:
        pass
    querystring = {"date": filtered_date}
    exists = mg.document_exists("match_results", querystring)
    if exists:
        fixture_document = mg.get_single_info("match_results", querystring)
        if fixture_document['is_unfinished']:
            return get_results_from_api(querystring, converted_date, filter_league, filtered_date)
        else:
            return fixture_document['results']
    else:
        return get_results_from_api(querystring, converted_date, filter_league, filtered_date)


def save_match_results(date_string, result_list, unfinished):
    count = mg.count_documents("match_results", {"date": date_string})
    results_for_date = {
        "date": date_string,
        "results": result_list,
        "is_unfinished": unfinished
    }
    if count == 0:
        mg.add_record("match_results", results_for_date)
    else:
        mg.update_record("match_results", {"date": date_string}, results_for_date)


def update_match_results(date_string, result_list, unfinished):
    count = mg.count_documents("match_results", {"date": date_string})
    results_for_date = {
        "date": date_string,
        "results": result_list,
        "is_unfinished": unfinished
    }
    if count == 0:
        mg.add_record("match_results", results_for_date)
    else:
        mg.update_record("match_results", {"date": date_string}, results_for_date)

def get_results_from_api(querystring, converted_date, filter_league, filtered_date):
    response = json.loads(api.get_request(url, querystring))
    today = datetime.now().date()
    the_date = converted_date.date()
    if the_date == today:
        status_array = ['FT', 'HT', 'NS', '1H', '2H', 'ET']
    else:
        status_array = ['FT']

    fixtures_list = []
    fixture_array = response['response']
    unfinished = False
    for idx, x in enumerate(fixture_array):
        if x['league']['id'] not in league_list and filter_league:
            del fixture_array[idx]
        else:
            pass
        fixture_status = x['fixture']['status']['short']
        date = x['fixture']['date']
        league_attr = leagues.check_league_attributes(x['league']['id'])
        if fixture_status in status_array:
            if fixture_status != 'FT':
                unfinished = True
            fixtures_list.append(build_results_list(league_attr, fixture_status, date, x))
    save_match_results(filtered_date, fixtures_list, unfinished)
    return fixtures_list


def build_results_list(league_attr, fixture_status, fixture_date, fixture):
    if fixture_status != 'FT':
        result_status = False
    else:
        result_status = True

    fixture_id = fixture['fixture']['id']
    # timestamp = x['fixture']['timestamp']
    venue_name = fixture['fixture']['venue']['name']
    venue_city = fixture['fixture']['venue']['city']

    league_id = fixture['league']['id']
    league_name = fixture['league']['name']
    league_country = fixture['league']['country']
    league_logo = fixture['league']['logo']
    league_flag = fixture['league']['flag']
    league_round = fixture['league']['round']

    home_team_id = fixture['teams']['home']['id']
    home_team_name = fixture['teams']['home']['name']
    home_team_goals = fixture['score']['fulltime']['home']
    home_team_logo = fixture['teams']['home']['logo']
    away_team_id = fixture['teams']['away']['id']
    away_team_name = fixture['teams']['away']['name']
    away_team_goals = fixture['score']['fulltime']['away']
    away_team_logo = fixture['teams']['away']['logo']

    fixture_json = {"fixture_id": fixture_id,
                    "fixture_status": fixture_status,
                    "league_id": league_id,
                    "league_name": league_name,
                    "league_country": league_country,
                    "league_logo": league_logo,
                    "league_flag": league_flag,
                    "league_attr": league_attr,
                    "fixture_time": get_date_time_split(fixture_date)[1],
                    "fixture_date": get_date_time_split(fixture_date)[0],
                    "round": league_round,
                    "location": f"{venue_name}, {venue_city}",
                    "home_name": home_team_name,
                    "home_goals": home_team_goals,
                    "home_id": home_team_id,
                    "home_logo": home_team_logo,
                    "away_name": away_team_name,
                    "away_goals": away_team_goals,
                    "away_id": away_team_id,
                    "away_logo": away_team_logo,
                    "is_unfinished": result_status}
    return fixture_json


def get_date_time_split(date):
    date = datetime.fromisoformat(date)
    match_time = date.strftime("%H:%M:%S")
    # match_date = date.strftime("%d-%m-%Y")
    match_date = date.strftime("%Y-%m-%d")
    return match_date, match_time