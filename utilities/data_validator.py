import json
from footy_api.models import Competition, AllMatches, PlayerEvent, Team
from datetime import datetime, timezone
from django.utils.dateparse import parse_datetime


def previous_match_validator(json_response):
    total = len(json_response['data'])
    for x in range(0, int(total)):
        match_id = json_response['data'][x]['id']
        match = AllMatches.objects.filter(id=int(match_id))
        if not match.exists():
            competition = json_response['data'][x]['competition_id']
            home_id = json_response['data'][x]['home_id']
            away_id = json_response['data'][x]['away_id']
            home_name = json_response['data'][x]['home_name']
            away_name = json_response['data'][x]['away_name']
            date = json_response['data'][x]['date']

            scheduled = json_response['data'][x]['scheduled']
            location = json_response['data'][x]['location']

            score = json_response['data'][x]['score']
            ht_score = json_response['data'][x]['ht_score']
            ft_score = json_response['data'][x]['ft_score']
            et_score = json_response['data'][x]['et_score']
            try:
                competition = Competition.objects.get(id=competition)
            except:
                competition = None
            try:
                home_team = Team.objects.get(id=home_id)
            except:
                home_team = None
            try:
                away_team = Team.objects.get(id=away_id)
            except:
                away_team = None

            if scheduled is not None:
                complete_date = date + ' ' + scheduled
            elif date is None:
                complete_date = None
            else:
                complete_date = date + ' 00:00'

            if location is None:
                location = ""

            new_date = parse_datetime(complete_date)

            restructured_data = {"home_id": home_team,
                                 "away_id": away_team,
                                 "date": new_date,
                                 "location": location,
                                 "competition": competition,
                                 "score": score,
                                 "ht_score": ht_score,
                                 "ft_score": ft_score,
                                 "et_score": et_score}
            if complete_date is None or home_team is None or away_team is None:
                return False
            else:
                return restructured_data
        else:
            return False


def team_exists_validator(home_id, away_id):
    home_team = Team.objects.get(id=home_id)
    away_team = Team.objects.get(id=away_id)

    if home_team is None or away_team is None:
        return False
    else:
        return True
