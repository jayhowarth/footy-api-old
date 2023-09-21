import requests
import json
from footy import config
# from utilities.counter import counter_inc
from utilities.previous_fixtures import update_teams_previous_matches
import datetime
import time
from datetime import datetime

match_url = "https://livescore-api.com/api-client/fixtures/matches.json"


def get_todays_fixtures():
    live_scores_url = match_url + "?" + config.live_scores_auth
    page_no = 1
    next_page = True
    fixtures_list = []
    while next_page:
        querystring = {"date": "today", "page": page_no}
        response = requests.get(live_scores_url, params=querystring)
        if response.status_code == 429:
            fixtures_list = "Reached 600 Limit per hour"
            time.sleep(3600)
            break
        json_response = response.json()
        page_no += 1
        total = len(json_response['data']['fixtures'])
        resp_next_page = json_response['data']['next_page']
        if not resp_next_page:
            next_page = False
        for x in range(0, int(total)):
            match_id = json_response['data']['fixtures'][x]['id']
            competition_id = json_response['data']['fixtures'][x]['competition_id']
            match_time = json_response['data']['fixtures'][x]['time']
            date = json_response['data']['fixtures'][x]['date']
            comp_round = json_response['data']['fixtures'][x]['round']
            location = json_response['data']['fixtures'][x]['location']
            home_name = json_response['data']['fixtures'][x]['home_name']
            home_id = json_response['data']['fixtures'][x]['home_id']
            update_teams_previous_matches(home_id)
            away_name = json_response['data']['fixtures'][x]['away_name']
            away_id = json_response['data']['fixtures'][x]['away_id']
            update_teams_previous_matches(away_id)
            odds_pre = json_response['data']['fixtures'][x]['odds']['pre']
            h2h_url = json_response['data']['fixtures'][x]['h2h']

            fixture_json = {"match_id": match_id,
                            "competition_id": competition_id,
                            "time": match_time,
                            "date": date,
                            "round": comp_round,
                            "location": location,
                            "home_name": home_name,
                            "home_id": home_id,
                            "away_name": away_name,
                            "away_id": away_id,
                            "odds_pre": odds_pre,
                            "h2h_url": h2h_url}
            fixtures_list.append(fixture_json)

    return fixtures_list


def get_tomorrows_fixtures():
    live_scores_url = match_url + "?" + config.live_scores_auth
    page_no = 1
    next_page = True
    fixtures_list = []
    format_data = "%y-%m-%d"
    date = datetime.date.today() + datetime.timedelta(days=1)
    tomorrows_date = date.strftime(format_data)
    while next_page:
        querystring = {"date": tomorrows_date, "page": page_no}
        response = requests.get(live_scores_url, params=querystring)
        if response.status_code == 429:
            fixtures_list = "Reached 600 Limit per hour"
            break
        json_response = response.json()
        page_no += 1
        total = len(json_response['data']['fixtures'])
        resp_next_page = json_response['data']['next_page']
        if not resp_next_page:
            next_page = False
        for x in range(0, int(total)):
            match_id = json_response['data']['fixtures'][x]['id']
            competition_id = json_response['data']['fixtures'][x]['competition_id']
            match_time = json_response['data']['fixtures'][x]['time']
            date = json_response['data']['fixtures'][x]['date']
            comp_round = json_response['data']['fixtures'][x]['round']
            location = json_response['data']['fixtures'][x]['location']
            home_name = json_response['data']['fixtures'][x]['home_name']
            home_id = json_response['data']['fixtures'][x]['home_id']
            update_teams_previous_matches(home_id)
            away_name = json_response['data']['fixtures'][x]['away_name']
            away_id = json_response['data']['fixtures'][x]['away_id']
            update_teams_previous_matches(away_id)
            odds_pre = json_response['data']['fixtures'][x]['odds']['pre']
            h2h_url = json_response['data']['fixtures'][x]['h2h']

            fixture_json = {"match_id": match_id,
                            "competition_id": competition_id,
                            "time": match_time,
                            "date": date,
                            "round": comp_round,
                            "location": location,
                            "home_name": home_name,
                            "home_id": home_id,
                            "away_name": away_name,
                            "away_id": away_id,
                            "odds_pre": odds_pre,
                            "h2h_url": h2h_url}
            fixtures_list.append(fixture_json)

    return fixtures_list

