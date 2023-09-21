from datetime import datetime
from utilities import mongo as mg


def team_fixture_update_entry(team_id, last_fixture, last_fixture_date, league_id, played_games):
    count = mg.count_documents("update", {"team_id": team_id})
    update_record = {
        "team_id": team_id,
        "league_id": league_id,
        "league_points": played_games,
        "last_fixture": last_fixture,
        "last_fixture_date": last_fixture_date,
        "last_updated": datetime.utcnow()
    }
    if count > 0:
        mg.update_record("update", {"team_id": team_id}, update_record)
    else:
        mg.add_record("update", update_record)