from utilities import mongo as mg
import json
from utilities import previous_fixtures


h2h_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"


def get_all_last_matches_for_team(team_id):
    query = [{"home_id": {"$eq": team_id}}, {"away_id": {"$eq": team_id}}]
    all_team_fixtures = mg.get_info_conditional_or("fixtures", query)
    team_fixtures = []
    for x in all_team_fixtures:
        team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)


def get_total_goals_in_list(matches_list):
    new_list = []
    for x in matches_list:
        total = int(x['score'][0]) + int(x['score'][-1])
        new_list.append({'date': x['date'],
                         'total_goals': total})
    return new_list


def get_last_x_matches(team_id, num):
    query = [{"home_id": {"$eq": team_id}}, {"away_id": {"$eq": team_id}}]
    all_team_fixtures = mg.get_info_conditional_or("fixtures", query)
    team_fixtures = []
    for x in all_team_fixtures:
        team_fixtures.append(x)
    return sorted(team_fixtures, key=lambda y: y['date'], reverse=True)[:num]





def get_last_x_goals(team_id, num_goals, num_matches):
    all_matches = get_last_x_matches(team_id, num_matches)
    goals_list = get_total_goals_in_list(all_matches)
    if num_goals > 0:
        x_goals = [x for x in goals_list if x['total_goals'] >= num_goals]
    else:
        x_goals = [x for x in goals_list if x['total_goals'] == num_goals]
    return x_goals


def get_x_goals_away(team_id, num_goals, num_matches):
    away_matches = get_last_x_away_matches(team_id, num_matches)
    goals_list = get_total_goals_in_list(away_matches)
    if num_goals > 0:
        x_goals = [x for x in goals_list if x['total_goals'] >= num_goals]
    else:
        x_goals = [x for x in goals_list if x['total_goals'] == num_goals]
    return x_goals


def get_x_goals_home(team_id, num_goals, num_matches):
    home_matches = get_last_x_home_matches(team_id, num_matches)
    goals_list = get_total_goals_in_list(home_matches)
    if num_goals > 0:
        x_goals = [x for x in goals_list if x['total_goals'] >= num_goals]
    else:
        x_goals = [x for x in goals_list if x['total_goals'] == num_goals]
    return x_goals


def get_btts(team_id, num_matches):
    all_matches = get_last_x_matches(team_id, num_matches)
    num_btts = [x for x in all_matches if int(x['score'][0]) > 0 and int(x['score'][-1]) > 0]
    return len(num_btts)


def get_btts_home(team_id, num_matches):
    all_matches = get_last_x_home_matches(team_id, num_matches)
    num_btts = [x for x in all_matches if int(x['score'][0]) > 0 and int(x['score'][-1]) > 0]
    return len(num_btts)


def get_btts_away(team_id, num_matches):
    all_matches = get_last_x_away_matches(team_id, num_matches)
    num_btts = [x for x in all_matches if int(x['score'][0]) > 0 and int(x['score'][-1]) > 0]
    return len(num_btts)


def get_cards(team_id, num_matches):
    all_matches = get_last_x_matches(team_id, num_matches)
    no_yellow = []
    no_red = []
    for x in all_matches:
        if x['statistics_home'] != {}:
            if x['statistics_home']['team_id'] == team_id:
                no_yellow.append(x['statistics_home']['statistics']['Yellow Cards'])
                no_red.append(x['statistics_home']['statistics']['Red Cards'])
            else:
                no_yellow.append(x['statistics_away']['statistics']['Yellow Cards'])
                no_red.append(x['statistics_away']['statistics']['Red Cards'])

    return no_yellow, no_red


def get_corners(team_id, num_matches):
    all_matches = get_last_x_matches(team_id, num_matches)
    no_corners = []
    for x in all_matches:
        if x['statistics_home'] != {}:
            if x['statistics_home']['team_id'] == team_id:
                no_corners.append(x['statistics_home']['statistics']['Corner Kicks'])
            else:
                no_corners.append(x['statistics_away']['statistics']['Corner Kicks'])

    return no_corners


def check_if_cup_competition(league_id):
    query = {"id": {"$eq": league_id}}
    league = mg.get_single_info("leagues", query)

    if league['type'] == "Cup":
        return True
    else:
        return False


def get_league_stats(league_id, team_id):
    query = {"id": {"$eq": league_id}}
    league = mg.get_single_info("standings", query)
    team_standing = [x for x in league['standings'] if x['team']['id'] == team_id]
    rank = team_standing[0]['rank']
    points = team_standing[0]['points']
    form = team_standing[0]['form']
    all_stats = team_standing[0]['all']
    home_stats = team_standing[0]['home']
    away_stats = team_standing[0]['away']
    goal_difference = team_standing[0]['goalsDiff']
    return {"position": rank,
            "form": form,
            "points": points,
            "gaol_diff": goal_difference,
            "all_stats": all_stats,
            "home_stats": home_stats,
            "away_stats": away_stats}


def get_previous_h2h_over_x_goals(home_team, away_team, num_goals):
    result = previous_fixtures.get_h2h_matches(home_team, away_team)
    number_of_prev_matches = len(result)
    goals_list = get_total_goals_in_list(result)
    x_goals = [x for x in goals_list if x['total_goals'] >= num_goals]
    return len(x_goals), number_of_prev_matches


def get_all_team_stats(team_id, num_matches):
    all_matches = get_last_x_matches(team_id, num_matches)
    stats = []
    for x in all_matches:
        if x['statistics_home'] != {}:
            if x['statistics_home']['team_id'] == team_id:
                team_stats = x['statistics_home']['statistics']
            else:
                team_stats = x['statistics_away']['statistics']
            corners = team_stats['Corner Kicks']
            yellow_cards = team_stats['Yellow Cards']
            red_cards = team_stats['Red Cards']
            possession = team_stats['Ball Possession']
            stats.append({
                "corners": corners,
                "yellow_cards": yellow_cards,
                "red_cards": red_cards,
                "possession": possession
            })
    return stats

