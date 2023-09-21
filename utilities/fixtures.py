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
        180, 181, 182, 183, 184, 185, 207, 208, 218, 219]

def get_todays_fixtures():
    date = f"{datetime.today().strftime('%Y-%m-%d')}"
    return get_fixtures_by_date(date, league_list)


def get_tomorrows_fixtures():
    tomorrow = date.today() + timedelta(days=1)
    date_string = f"{tomorrow.strftime('%Y-%m-%d')}"
    return get_fixtures_by_date(date_string)


# def get_all_todays_fixtures():
#     date = f"{datetime.today().strftime('%Y-%m-%d')}"
#     return get_all_fixtures_by_date(date)


def get_date_time_split(date):
    date = datetime.fromisoformat(date)
    match_time = date.strftime("%H:%M:%S")
    # match_date = date.strftime("%d-%m-%Y")
    match_date = date.strftime("%Y-%m-%d")
    return match_date, match_time


def save_upcoming_fixtures(date_string, fixture_list):
    count = mg.count_documents("upcoming_fixtures", {"date": date_string})
    daily_fixture = {
        "date": date_string,
        "fixtures": fixture_list
    }
    if count == 0:
        mg.add_record("upcoming_fixtures", daily_fixture)
    else:
        mg.update_record("upcoming_fixtures", {"date": date_string}, daily_fixture)


def get_fixtures_by_date(fixture_date, filter_league):
    converted_date = parser.parse(fixture_date)
    ppf = past_present_future(converted_date)
    filtered_date = converted_date.strftime('%Y-%m-%d')
    if filter_league:
        filter_league = league_list
    else:
        pass
    querystring = {"date": filtered_date}
    exists = mg.document_exists("upcoming_fixtures", querystring)
    if exists:
        fixture_document = mg.get_single_info("upcoming_fixtures", querystring)
        return fixture_document['fixtures']
    else:
        #if not in database
        response = json.loads(api.get_request(url, querystring))
        if ppf == 'past':
            status_array = ['FT']
        elif ppf == 'present':
            status_array = ['FT', 'HT', 'NS', '1H', '2H', 'ET']
        else:
            status_array = ['NS']
        x_status_array = ['FT', 'CANC', 'ABD', 'TBD']
        fixtures_list = []
        fixture_array = response['response']

        for idx, x in enumerate(fixture_array):
            if x['league']['id'] not in league_list and filter_league:
                del fixture_array[idx]
            else:
                pass
            fixture_status = x['fixture']['status']['short']
            date = x['fixture']['date']
            league_attr = leagues.check_league_attributes(x['league']['id'])
            fixture_date = datetime.fromisoformat(date)
            fixture_in_future = timezone.now() < fixture_date
            if fixture_status in status_array:
                # fixture_id = x['fixture']['id']
                # #timestamp = x['fixture']['timestamp']
                # venue_name = x['fixture']['venue']['name']
                # venue_city = x['fixture']['venue']['city']
                #
                # league_id = x['league']['id']
                # league_name = x['league']['name']
                # league_country = x['league']['country']
                # league_logo = x['league']['logo']
                # league_flag = x['league']['flag']
                # league_round = x['league']['round']
                #
                # home_team_id = x['teams']['home']['id']
                # home_team_name = x['teams']['home']['name']
                # home_team_logo = x['teams']['home']['logo']
                # away_team_id = x['teams']['away']['id']
                # away_team_name = x['teams']['away']['name']
                # away_team_logo = x['teams']['away']['logo']
                #
                # fixture_json = {"fixture_id": fixture_id,
                #                 "fixture_status": fixture_status,
                #                 "league_id": league_id,
                #                 "league_name": league_name,
                #                 "league_country": league_country,
                #                 "league_logo": league_logo,
                #                 "league_flag": league_flag,
                #                 "league_attr": league_attr,
                #                 "fixture_time": get_date_time_split(date)[1],
                #                 "fixture_date": get_date_time_split(date)[0],
                #                 "round": league_round,
                #                 "location": f"{venue_name}, {venue_city}",
                #                 "home_name": home_team_name,
                #                 "home_id": home_team_id,
                #                 "home_logo": home_team_logo,
                #                 "away_name": away_team_name,
                #                 "away_id": away_team_id,
                #                 "away_logo": away_team_logo}
                fixtures_list.append(build_fixture_list(league_attr, fixture_status,date, x))
        save_upcoming_fixtures(filtered_date, fixtures_list)
        return fixtures_list


def get_past_fixtures(fixture_date):
    pass


def get_inplay_fixtures(fixture_date):
    pass


def get_future_fixtures(fixture_date):
    pass


def build_fixture_list(league_attr, fixture_status, fixture_date, fixture):
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
    home_team_logo = fixture['teams']['home']['logo']
    away_team_id = fixture['teams']['away']['id']
    away_team_name = fixture['teams']['away']['name']
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
                    "home_id": home_team_id,
                    "home_logo": home_team_logo,
                    "away_name": away_team_name,
                    "away_id": away_team_id,
                    "away_logo": away_team_logo}
    return fixture_json

def past_present_future(date):
    today = datetime.now().date()
    fixture_date = date.date()
    if fixture_date == today:
        return "current"
    elif fixture_date < today:
        return "past"
    else:
        return "future"

# def get_all_fixtures_by_date(date):
#     querystring = {"date": date}
#     response = json.loads(api.get_request(url, querystring))
#     all_fixtures_list = []
#     fixture_array = response['response']
#     for x in fixture_array:
#         fixture_status = x['fixture']['status']['short']
#         date = x['fixture']['date']
#         fixture_id = x['fixture']['id']
#         #timestamp = x['fixture']['timestamp']
#         venue_name = x['fixture']['venue']['name']
#         venue_city = x['fixture']['venue']['city']
#
#         league_id = x['league']['id']
#         league_name = x['league']['name']
#         league_country = x['league']['country']
#         league_logo = x['league']['logo']
#         league_flag = x['league']['flag']
#         league_round = x['league']['round']
#
#         home_team_id = x['teams']['home']['id']
#         home_team_name = x['teams']['home']['name']
#         home_team_logo = x['teams']['home']['logo']
#         away_team_id = x['teams']['away']['id']
#         away_team_name = x['teams']['away']['name']
#         away_team_logo = x['teams']['away']['logo']
#
#         fixture_json = {"fixture_id": fixture_id,
#                         "fixture_status": fixture_status,
#                         "league_id": league_id,
#                         "league_name": league_name,
#                         "league_country": league_country,
#                         "league_logo": league_logo,
#                         "league_flag": league_flag,
#                         "time": get_date_time_split(date)[1],
#                         "date": get_date_time_split(date)[0],
#                         "round": league_round,
#                         "location": f"{venue_name}, {venue_city}",
#                         "home_name": home_team_name,
#                         "home_id": home_team_id,
#                         "home_logo": home_team_logo,
#                         "away_name": away_team_name,
#                         "away_id": away_team_id,
#                         "away_logo": away_team_logo}
#         all_fixtures_list.append(fixture_json)
#
#     return all_fixtures_list

