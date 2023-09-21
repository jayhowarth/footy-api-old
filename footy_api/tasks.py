from footy import celery
from utilities import fixtures
from utilities import league_standings as stand
from utilities import previous_fixtures as prev
from utilities.leagues import check_if_league, get_league_and_country_by_id
from utilities.league_standings import update_league_standings_by_league
from utilities.teams import check_when_last_team_fixtures_updated, add_one_team
from utilities.redis_manager import RedisManager as r

league_list = [39, 40, 41, 42, 43, 45, 48,
               135, 136, 137, 140, 141, 143, 61, 62, 66, 88,
               89, 78, 79, 80, 94, 97,
               103, 104, 113, 114, 115, 119, 120, 144, 145, 147, 179,
               180, 181, 182, 183, 184, 185, 207, 208, 218, 219]


@celery.app.task
def update_previous_matches():
    all_fixtures = fixtures.get_todays_fixtures(league_list)
    total_added = 0
    home_added = 0
    away_added = 0
    h2h_added = 0
    total_fixtures = len(all_fixtures)
    for idx, x in enumerate(all_fixtures):
        home_updated = prev.check_when_last_team_fixtures_updated(x['home_id'])
        away_updated = prev.check_when_last_team_fixtures_updated(x['away_id'])
        if home_updated:
            home = prev.add_previous_matches(x['home_id'])
            home_added = home[0]
        if away_updated:
            away = prev.add_previous_matches(x['away_id'])
            away_added = away[0]
        if home_updated and away_updated:
            h2h_added = prev.get_h2h_matches(x['home_id'], x['away_id'])
        total_added += (home_added + away_added + h2h_added)
        print('Remaining: ' + str(r.get_remaining_counter()))
        print(str(idx + 1) + ' of ' + str(total_fixtures) + ': ' + x['home_name'] + ' vs ' + x['away_name'])
    print(f'{total_added} total matches added')


@celery.app.task
def update_h2h_for_todays_matches():
    all_fixtures = fixtures.get_todays_fixtures(league_list)
    total_added = 0
    for idx, x in enumerate(all_fixtures):
        h2h_added = prev.get_h2h_matches(x['home_id'], x['away_id'])
        print('Remaining: ' + str(r.get_remaining_counter()))
        total_added += h2h_added
    print(f'{total_added} total matches added')


@celery.app.task
def update_all_previous_matches_for_league(league_id):
    standings = stand.all_teams_in_league(league_id)
    total_added = 0
    for x in standings:
        needs_updating = prev.check_when_last_team_fixtures_updated(x['team']['id'])
        if needs_updating:
            team = prev.add_previous_matches(x['team']['id'])
            total_added += team[0]
        print('Remaining: ' + str(r.get_remaining_counter()))
        print(f"Updated matches for {x['team']['name']}")
    print(f'{total_added} total matches added')


@celery.app.task
def update_all_previous_matches_for_selected_leagues():
    total_added = 0
    for league in league_list:
        if check_if_league(league):
            standings = stand.all_teams_in_league(league)
            for x in standings:
                needs_updating = prev.check_when_last_team_fixtures_updated(x['team']['id'])
                if needs_updating:
                    team = prev.add_previous_matches(x['team']['id'])
                    total_added += team[0]
                print('Remaining: ' + str(r.get_remaining_counter()))
                print(f"Updated matches for {x['team']['name']}")
        else:
            print('Is Cup')
    print(f'{total_added} total matches added')


@celery.app.task
def update_selected_league_tables():
    league_list = [39, 40, 41, 42, 43, 45, 48,
                   135, 136, 137, 140, 141, 143, 61, 62, 66, 88,
                   89, 78, 79, 80, 94, 97,
                   103, 104, 113, 114, 115, 119, 120, 144, 145, 147, 179,
                   180, 181, 182, 183, 184, 185, 207, 208, 218, 219]
    for league in league_list:
        update_league_standings_by_league(league)
        item = get_league_and_country_by_id(league)
        print(f'Updated {item}')
