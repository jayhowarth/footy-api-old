from archive import calc_team_statistics as stat, points_calc as calc


def probability_over_x(home_team_id, away_team_id, num_over):
    total = 0
    max_total = 0
    # Calculate last 5 games over 1.5 goals points multiplied by 2 #
    x = calc.last_5_over_x_points_calc(home_team_id, num_over)
    total += x
    max_total += 10
    x = calc.last_5_over_x_points_calc(away_team_id, num_over)
    total += x
    max_total += 10

    # Calculate last 10 games over 1.5 goals points #
    x = calc.last_10_over_x_points_calc(home_team_id, num_over)
    total += x
    max_total += 10
    x = calc.last_10_over_x_points_calc(away_team_id, num_over)
    total += x
    max_total += 10

    # Calculate last 5 home/away games over 1.5 goals points #
    x = calc.last_5_home_over_x_points_calc(home_team_id, num_over)
    total += x
    max_total += 5
    x = calc.last_5_away_over_x_points_calc(away_team_id, num_over)
    total += x
    max_total += 5

    # Calculate last 5 games over 2.5 goals points multiplied by 1.5 #
    x = calc.last_5_over_x_points_calc(home_team_id, num_over + 1)
    total += (x*1.5)
    max_total += 15
    x = calc.last_5_over_x_points_calc(away_team_id, num_over + 1)
    total += (x*1.5)
    max_total += 15

    # check if in same country/league, difference in league position
    if stat.check_teams_in_same_country(home_team_id, away_team_id):
        if stat.check_teams_in_same_competition(home_team_id, away_team_id):
            x, x_max = calc.difference_in_league_position(home_team_id, away_team_id)
            total += x
            max_total += x_max - 1

    # check for 0-0 draws number of them in last 5 multiplied by 10 #
    x = calc.nil_draws_in_last_5(home_team_id)
    total += x
    x = calc.nil_draws_in_last_5(away_team_id)
    total += x

    # get previous matches in last x multiplied by 2 #
    x, x_max = stat.get_previous_h2h_over_x_goals(home_team_id, away_team_id, num_over)
    total += (x*2)
    max_total += (x_max*2)

    x = calc.average_goals_diff_calc(home_team_id)
    total += x
    max_total += 13

    x = calc.average_goals_diff_calc(away_team_id)
    total += x
    max_total += 13

    return round((total/max_total)*100)


def probability_over_2_5(home_team_id, away_team_id):
    total = 0
    x = calc.last_5_over_x_points_calc(home_team_id, 3)
    total += x
    x = calc.last_5_over_x_points_calc(away_team_id, 3)
    total += x
