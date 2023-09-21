from archive import calc_team_statistics as stat


def last_5_over_x_points_calc(team_id, num_goals):
    result = stat.get_last_x_goals(team_id, num_goals, 5)
    return len(result) * 2


def last_10_over_x_points_calc(team_id, num_goals):
    result = stat.get_last_x_goals(team_id, num_goals, 10)
    return len(result)


def last_5_home_over_x_points_calc(team_id, num_goals):
    result = stat.get_x_goals_home(team_id, num_goals, 5)
    return len(result)


def last_5_away_over_x_points_calc(team_id, num_goals):
    result = stat.get_x_goals_away(team_id, num_goals, 5)
    return len(result)


def difference_in_league_position(home_id, away_id):
    home_stats = stat.get_league_stats(home_id)
    away_stats = stat.get_league_stats(away_id)
    total_teams = home_stats['teams_in_league']
    diff_position = 0
    if home_stats['played'] >= 5 and away_stats['played'] >= 5:
        diff_position = home_stats['position'] - away_stats['position']
        return abs(diff_position), total_teams
    else:
        diff_position = 5
        return diff_position, total_teams


def nil_draws_in_last_5(team_id):
    result = stat.get_last_x_goals(team_id, 0, 5)
    return -(10 * len(result))


def average_goals_diff_calc(team_id):
    stats = stat.get_league_stats(team_id)
    total_played = stats['played']
    if total_played > 4:
        total_scored = stats['goals_scored']
        total_conceded = stats['goals_conceded']
        average_goals_scored = total_scored / total_played
        average_goals_conceded = total_conceded / total_played
        if average_goals_scored < 1 and average_goals_conceded < 1:
            return 0
        elif 1 <= average_goals_scored < 1.5 and 1 <= average_goals_conceded < 1.5:
            return 2
        elif average_goals_scored < 1.3 and 1 >= average_goals_conceded < 2:
            return 5
        elif average_goals_scored < 1.3 and 2 >= average_goals_conceded < 3:
            return 8
        elif average_goals_scored < 1.3 and average_goals_conceded > 3:
            return 13
        elif 1 <= average_goals_scored < 1.5 and average_goals_conceded < 1.3:
            return 2
        elif 1.5 >= average_goals_scored < 2 and average_goals_conceded < 1.3:
            return 3
        elif 2 >= average_goals_scored < 2 and average_goals_conceded < 1.3:
            return 5
        elif 2 >= average_goals_scored < 3 and average_goals_conceded < 1.3:
            return 8
        elif average_goals_scored > 3 and average_goals_conceded < 1.3:
            return 13
        elif 1.5 > average_goals_scored <= 2 and 1.5 > average_goals_conceded <= 2:
            return 5
        elif 1.5 > average_goals_scored <= 2 and average_goals_conceded  > 2:
            return 8
        elif average_goals_scored > 2 and 1.5 > average_goals_conceded <= 2:
            return 8
        elif average_goals_scored > 2 and average_goals_conceded > 2:
            return 13
        elif average_goals_scored > 4 or average_goals_conceded > 4:
            return 20
    else:
        return 3



