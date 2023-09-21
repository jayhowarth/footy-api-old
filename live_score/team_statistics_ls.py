import requests, json
from footy import config
from footy_api.models import Competition, AllMatches, PlayerEvent, Team, LeagueStandings
from django.db.models import Q

h2h_url = "https://livescore-api.com/api-client/teams/head2head.json"


def get_total_goals_in_list(matches_list):
    new_list = []
    for x in matches_list:
        total = int(x['score'][0]) + int(x['score'][-1])
        new_list.append({'date': x['date'],
                         'total_goals': total})
    return new_list


def get_last_x_matches(team_id, x):
    team = Team.objects.get(id=team_id)
    team_matches = AllMatches.objects.filter(Q(home_team=team) | Q(away_team=team)).values()
    return sorted(list(team_matches), key=lambda y: y['date'], reverse=True)[:x]


def get_last_x_home_matches(team_id, x):
    team = Team.objects.get(id=team_id)
    home_team_matches = AllMatches.objects.filter(home_team=team).values()
    return sorted(list(home_team_matches), key=lambda y: y['date'], reverse=True)[:x]


def get_last_x_away_matches(team_id, x):
    team = Team.objects.get(id=team_id)
    away_team_matches = AllMatches.objects.filter(away_team=team).values()
    return sorted(list(away_team_matches), key=lambda y: y['date'], reverse=True)[:x]


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


def check_teams_in_same_competition(home_team, away_team):
    home_league = LeagueStandings.objects.filter(team_id=home_team).values('competition')
    away_league = LeagueStandings.objects.filter(team_id=away_team).values('competition')
    if home_league[0]['competition'] == away_league[0]['competition']:
        return True
    else:
        return False


def check_teams_in_same_country(home_team, away_team):
    home_league = LeagueStandings.objects.filter(team_id=home_team).values('competition')
    home_country = Competition.objects.filter(id=home_league[0]['competition']).values('country')
    away_league = LeagueStandings.objects.filter(team_id=away_team).values('competition')
    away_country = Competition.objects.filter(id=away_league[0]['competition']).values('country')

    if home_country[0]['country'] == away_country[0]['country']:
        return True
    else:
        return False


def get_league_stats(team_id):

    league_standing = LeagueStandings.objects.filter(team_id=team_id).values()
    competition = league_standing[0]['competition_id']
    league_teams = LeagueStandings.objects.filter(competition_id=competition).values()
    position = league_standing[0]['rank']
    played = league_standing[0]['matches']
    won = league_standing[0]['won']
    drawn = league_standing[0]['drawn']
    lost = league_standing[0]['lost']
    goals_scored = league_standing[0]['goals_scored']
    goals_conceded = league_standing[0]['goals_conceded']
    goal_difference = league_standing[0]['goal_diff']
    return {"position": int(position),
            "played": int(played),
            "won": int(won),
            "drawn": int(drawn),
            "lost": int(lost),
            "goals_scored": int(goals_scored),
            "goals_conceded": int(goals_conceded),
            "goal_difference": int(goal_difference),
            "teams_in_league": len(league_teams)}


def get_head_2_head(home_id, away_id):
    h2h_scores_url = h2h_url + "?" + config.live_scores_auth
    querystring = {"team1_id": home_id, "team2_id": away_id}
    response = requests.get(h2h_scores_url, params=querystring)
    json_response = response.json()
    team1_id = json_response['data']['team1']['id']
    team1_name = json_response['data']['team1']['name']
    team1_stadium = json_response['data']['team1']['stadium']
    team1_overall_form = json_response['data']['team1']['overall_form']
    team1_h2h_form = json_response['data']['team1']['h2h_form']
    team2_id = json_response['data']['team2']['id']
    team2_name = json_response['data']['team2']['name']
    team2_stadium = json_response['data']['team2']['stadium']
    team2_overall_form = json_response['data']['team2']['overall_form']
    team2_h2h_form = json_response['data']['team2']['h2h_form']
    h2h_list = json_response['data']['h2h']

    h2h_json = {"team1_id": team1_id,
                "team1_name": team1_name,
                "team1_stadium": team1_stadium,
                "team1_overall_form": team1_overall_form,
                "team1_h2h_form": team1_h2h_form,
                "team2_id": team2_id,
                "team2_name": team2_name,
                "team2_stadium": team2_stadium,
                "team2_overall_form": team2_overall_form,
                "team2_h2h_form": team2_h2h_form,
                "overall_h2h": h2h_list}
    #h2h_list.append(h2h_json)

    return h2h_json


def get_previous_h2h_over_x_goals(home_team, away_team, num_goals):
    result = get_head_2_head(home_team, away_team)
    h2h_list = result['overall_h2h']
    number_of_prev_matches = len(h2h_list)
    goals_list = get_total_goals_in_list(h2h_list)
    x_goals = [x for x in goals_list if x['total_goals'] >= num_goals]
    return len(x_goals), number_of_prev_matches


