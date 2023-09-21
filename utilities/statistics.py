import json
from datetime import datetime

from utilities import mongo as mg
import bson.json_util as json_util
from utilities import league_standings, leagues
import numpy as np


h2h_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"


def get_all_last_matches_for_team(team_id, num):
    query = [{"home_id": {"$eq": team_id}}, {"away_id": {"$eq": team_id}}]
    all_team_fixtures = mg.get_info_conditional_or("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)

def get_all_last_league_matches_for_team(team_id, num):
    query = [{"home_id": {"$eq": team_id}}, {"away_id": {"$eq": team_id}}]
    all_team_fixtures = mg.get_info_conditional_or("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        if leagues.check_if_league(x["league_id"]):
            team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)

def get_last_x_home_matches(team_id, num):
    query = {"home_id": {"$eq": team_id}}
    all_team_fixtures = mg.get_multiple_info("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)

def get_last_x_home_league_matches(team_id, num):
    query = {"home_id": {"$eq": team_id}}
    all_team_fixtures = mg.get_multiple_info("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        if leagues.check_if_league(x["league_id"]):
            team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)

def get_last_x_away_matches(team_id, num):
    query = {"away_id": {"$eq": team_id}}
    all_team_fixtures = mg.get_multiple_info("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)

def get_last_x_away_league_matches(team_id, num):
    query = {"away_id": {"$eq": team_id}}
    all_team_fixtures = mg.get_multiple_info("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        if leagues.check_if_league(x["league_id"]):
            team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)
###################

def get_last_league_matches_for_team(team_id, league_only, h_d_all, num):
    if h_d_all == "home":
        query = {"home_id": {"$eq": team_id}}
    elif h_d_all == "away":
        query = {"away_id": {"$eq": team_id}}
    else:
        query = [{"home_id": {"$eq": team_id}}, {"away_id": {"$eq": team_id}}]
    all_team_fixtures = mg.get_info_conditional_or("fixtures", query)
    sorted_fixtures = sorted(all_team_fixtures, key=lambda y: y['date'], reverse=True)
    team_fixtures = []
    for x in sorted_fixtures[:num]:
        if league_only:
            if leagues.check_if_league(x["league_id"]):
                team_fixtures.append(x)
        else:
            team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)

##################

def get_all_h2h(home_team, away_team):
    query1 = [{"home_id": {"$eq": home_team}}, {"away_id": {"$eq": away_team}}]
    query2 = [{"home_id": {"$eq": away_team}}, {"away_id": {"$eq": home_team}}]
    all_h2h_home = mg.get_info_conditional_and("fixtures", query1)
    all_h2h_away = mg.get_info_conditional_and("fixtures", query2)
    sorted_fixtures = sorted(all_h2h_home + all_h2h_away, key=lambda y: y['date'], reverse=True)
    return sorted_fixtures



### Win Lose Draw ###

def get_total_W_L_D_for_team(matches_list, team_id):
    new_list = []
    for x in matches_list:
        if x['score']['fulltime']['home'] == x['score']['fulltime']['away']:
            new_list.append("D")
        elif x['home_id'] == team_id:
            if x['score']['fulltime']['home'] > x['score']['fulltime']['away']:
                new_list.append("W")
            else:
                new_list.append("L")
        else:
            if x['score']['fulltime']['home'] > x['score']['fulltime']['away']:
                new_list.append("L")
            else:
                new_list.append("W")

    return new_list

def get_W_L_D_for_team_in_league(matches_list, team_id):
    new_list = []
    for x in matches_list:
        is_league_game = leagues.check_if_league(x['league_id'])
        if is_league_game:
            if x['score']['fulltime']['home'] == x['score']['fulltime']['away']:
                new_list.append("D")
            elif x['home_id'] == team_id:
                if x['score']['fulltime']['home'] > x['score']['fulltime']['away']:
                    new_list.append("W")
                else:
                    new_list.append("L")
            else:
                if x['score']['fulltime']['home'] > x['score']['fulltime']['away']:
                    new_list.append("L")
                else:
                    new_list.append("W")

    return new_list

def get_total_goals_in_list(matches_list):
    new_list = []
    for x in matches_list:
        total = int(x['score']['fulltime']['home']) + int(x['score']['fulltime']['away'])
        new_list.append(total)
    return new_list

def get_team_goals_scored_in_list(matches_list, team_id):
    new_list = []
    for x in matches_list:
        if x['home_id'] == team_id:
            new_list.append(int(x['score']['fulltime']['home']) )
        else:
            new_list.append(int(x['score']['fulltime']['away']))
    return new_list

def get_home_away_team_goals_scored_in_list(matches_list, team_id):
    new_list = []
    for x in matches_list:
        if x['home_id'] == team_id:
            new_list.append(int(x['score']['fulltime']['home']) )
        else:
            new_list.append(int(x['score']['fulltime']['away']))
    return new_list


### Cards ###

def get_players_with_most_cards(team_id):
    query = {"statistics.team.id": {"$eq": team_id}}
    players = mg.get_multiple_info("players", query)
    total_cards = []
    for player in players:
        yellow = 0
        red = 0
        yellow_red = 0
        booking_pts = 0
        for cards in player['statistics']:
            if cards['league'] != "Club Friendly":
                all = cards['cards']
                try:
                    yellow += all['yellow']
                    red += all['red']
                    yellow_red += all['yellowred']
                    booking_pts += all['yellow'] + 2*all['red'] + 2*all['yellowred']
                except TypeError:
                    pass
        total_cards.append({'name': player['name'],
                      'injured': player['injured'],
                      'yellow': yellow,
                      'yellow_red': yellow_red,
                      'red': red,
                      'booking_pts': booking_pts})
    def get_booking_pts(element):
        return element['booking_pts']

    x = sorted(total_cards, key=get_booking_pts, reverse=True)
    return x[:10]

### Goals ###
def get_total_match_no_goals_for_team(all_matches):
    goals_list = []
    for x in all_matches:
        if x['score']['fulltime']['home'] + x['score']['fulltime']['away'] == 0:
            goals_list.append(True)
        else:
            goals_list.append(False)
    return goals_list

def get_total_match_goals_over_1_5_for_team(all_matches):
    goals_list = []
    for x in all_matches:
        if x['score']['fulltime']['home'] + x['score']['fulltime']['away'] > 1:
            goals_list.append(True)
        else:
            goals_list.append(False)
    return goals_list

def get_total_match_goals_over_2_5_for_team(all_matches):
    goals_list = []
    for x in all_matches:
        if x['score']['fulltime']['home'] + x['score']['fulltime']['away'] > 2:
            goals_list.append(True)
        else:
            goals_list.append(False)
    return goals_list

def get_total_match_goals_over_3_5_for_team(all_matches):
    goals_list = []
    for x in all_matches:
        if x['score']['fulltime']['home'] + x['score']['fulltime']['away'] > 3:
            goals_list.append(True)
        else:
            goals_list.append(False)
    return goals_list

def get_total_number_of_match_goals_for_team(all_matches):
    pass

def get_number_of_team_goals_in_last_matches(team_id):
    pass


def get_number_of_total_h2h_goals(team1_id, team2_id):
    pass

def get_btts_in_last_matches(all_matches):
    # num_btts = [x for x in all_matches if x['score']['fulltime']['home'] > 0 and x['score']['fulltime']['away'] > 0]
    btts_list = []
    for x in all_matches:
        if x['score']['fulltime']['home'] > 0 and x['score']['fulltime']['away'] > 0:
            btts_list.append(True)
        else:
            btts_list.append(False)
    return btts_list

def get_btts_no_draw_in_last_matches(team_id):
    pass

##### League Standings #####

def get_league_standings_stats(team_id, league_id):
    standings = league_standings.all_teams_in_league(league_id)
    return [x for x in standings if x['team']['id'] == team_id][0]

##########################

def return_team_stats(team_id, num):
    match_list = get_all_last_matches_for_team(team_id)[:num]
    goals = get_total_goals_in_list(match_list)
    return goals

def return_team_stats(matches, all_home_away_matches, team_id):
    cards = get_players_with_most_cards(team_id)

    ##### All Matches ####
    wld = get_total_W_L_D_for_team(matches, team_id)
    # wld_league = get_W_L_D_for_team_in_league(matches, team_id)
    no_goals = get_total_match_no_goals_for_team(matches)
    goals_over_1_5 = get_total_match_goals_over_1_5_for_team(matches)
    goals_over_2_5 = get_total_match_goals_over_2_5_for_team(matches)
    goals_over_3_5 = get_total_match_goals_over_3_5_for_team(matches)
    btts = get_btts_in_last_matches(matches)
    match_average_goals = np.average(get_total_goals_in_list(matches))
    team_average_match_goals = np.average(get_team_goals_scored_in_list(matches, team_id))

    ##### Home/Away Matches ####
    ha_wld = get_total_W_L_D_for_team(all_home_away_matches, team_id)
    # ha_wld_league = get_W_L_D_for_team_in_league(all_home_away_matches, team_id)
    ha_no_goals = get_total_match_no_goals_for_team(all_home_away_matches)
    ha_goals_over_1_5 = get_total_match_goals_over_1_5_for_team(all_home_away_matches)
    ha_goals_over_2_5 = get_total_match_goals_over_2_5_for_team(all_home_away_matches)
    ha_goals_over_3_5 = get_total_match_goals_over_3_5_for_team(all_home_away_matches)
    ha_btts = get_btts_in_last_matches(all_home_away_matches)
    ha_match_average_goals = np.average(get_total_goals_in_list(all_home_away_matches))
    ha_team_average_match_goals = np.average(get_team_goals_scored_in_list(all_home_away_matches, team_id))

    return {
        "cards": cards,
        "wld": wld,
        "ha_wld": ha_wld,
        "btts": btts,
        "ha_btts": ha_btts,
        "no_goals": no_goals,
        "ha_no_goals": ha_no_goals,
        "over_1_5": goals_over_1_5,
        "ha_over_1_5": ha_goals_over_1_5,
        "over_2_5": goals_over_2_5,
        "ha_over_2_5": ha_goals_over_2_5,
        "over_3_5": goals_over_3_5,
        "ha_over_3_5": ha_goals_over_3_5,
        "team_average_goals": match_average_goals,
        "ha_team_average_goals": ha_match_average_goals,
        "match_average_goals": team_average_match_goals,
        "ha_match_average_goals": ha_team_average_match_goals
    }


def return_combined_team_stats(fixture_id, home_team_id, away_team_id):

    if not mg.document_exists("upcoming_statistics", {"fixture_id": fixture_id}):
        #### All Matches ####
        all_home_team_matches = get_all_last_matches_for_team(home_team_id, 10)
        all_away_team_matches = get_all_last_matches_for_team(away_team_id, 10)

        all_home_team_home_matches = get_last_x_home_matches(home_team_id, 10)
        all_away_team_away_matches = get_last_x_away_matches(away_team_id, 10)
        data = {
            "fixture_id": fixture_id,
            "date": datetime.utcnow(),
            "home": return_team_stats(all_home_team_matches, all_home_team_home_matches, home_team_id),
            "away": return_team_stats(all_away_team_matches, all_away_team_away_matches, away_team_id)
        }
        mg.add_record("upcoming_statistics", data)
        return data
    else:
        x =  mg.get_single_info("upcoming_statistics", {"fixture_id": fixture_id})
        return x


