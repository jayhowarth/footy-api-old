import requests
from django.utils.dateparse import parse_datetime
from footy_api.models import Competition, AllMatches, PlayerEvent, Team
from datetime import timezone

from archive.counter import counter_inc
from footy import config

matches_url = "https://livescore-api.com/api-client/teams/matches.json"
event_url = 'https://livescore-api.com/api-client/scores/events.json'

main_comp_ids = ["1", "2", "3", "4", "5", "244", "245"]
# client = Client('localhost')
# client.set('api_calls', 0)


def update_teams_previous_matches(team_id):
    live_scores_url = matches_url + "?" + config.live_scores_auth
    response = requests.get(live_scores_url, params={"team_id": str(team_id), "number": 30})
    counter_inc()

    json_response = response.json()
    total = len(json_response['data'])
    no_matches_added = 0

    if json_response['data']:
        for x in range(0, int(total)):
            match_id = json_response['data'][x]['id']
            match = AllMatches.objects.filter(id=int(match_id))
            competition = json_response['data'][x]['competition_id']
            home_id = json_response['data'][x]['home_id']
            away_id = json_response['data'][x]['away_id']
            home_name = json_response['data'][x]['home_name']
            away_name = json_response['data'][x]['away_name']
            date = json_response['data'][x]['date']

            if not match.exists():
                scheduled = json_response['data'][x]['scheduled']
                location = json_response['data'][x]['location']
                try:
                    home_team = Team.objects.get(id=home_id)
                except:
                    home_team = None
                try:
                    away_team = Team.objects.get(id=away_id)
                except:
                    away_team = None
                score = json_response['data'][x]['score']
                ht_score = json_response['data'][x]['ht_score']
                ft_score = json_response['data'][x]['ft_score']
                et_score = json_response['data'][x]['et_score']
                try:
                    competition = Competition.objects.get(id=competition)
                except:
                    competition = None

                if scheduled is not None:
                    complete_date = date + ' ' + scheduled
                else:
                    complete_date = date + ' 00:00'

                if location is None:
                    location = ""

                new_date = parse_datetime(complete_date)

                matches = AllMatches(id=match_id,
                                     competition=competition,
                                     date=new_date.replace(tzinfo=timezone.utc),
                                     location=location,
                                     home_team=home_team,
                                     away_team=away_team,
                                     score=score,
                                     ht_score=ht_score,
                                     ft_score=ft_score,
                                     et_score=et_score)
                matches.save()
                if str(competition.id) in main_comp_ids:
                    get_fixture_events(match_id, date, home_id, away_id)
                no_matches_added += 1
            else:
                if competition in main_comp_ids:
                    match_in_event = PlayerEvent.objects.filter(match=match_id)
                    if not match_in_event.exists():
                        get_fixture_events(match_id, date, home_id, away_id)

        return no_matches_added
    else:
        return "No Previous Match Data"


def get_fixture_events(match_id, date, h, a):
    events_url = event_url + "?" + config.live_scores_auth
    response = requests.get(events_url, params={"id": str(match_id)})
    counter_inc()
    new_date = parse_datetime(date)
    json_response = response.json()
    total = len(json_response['data']['event'])
    events_added = 0
    if json_response['data']['event']:
        for x in range(0, int(total)):
            event_id = json_response['data']['event'][x]['id']
            event = PlayerEvent.objects.filter(id=str(event_id))

            if not event.exists():
                temp_player = json_response['data']['event'][x]['player'].title()
                player = temp_player.replace(" ", ", ", 1)
                match = AllMatches.objects.get(id=match_id)
                temp_event = json_response['data']['event'][x]['event'].title()
                event = temp_event.replace("_", " ")
                time = json_response['data']['event'][x]['time']
                home_away = json_response['data']['event'][x]['home_away']
                if home_away == "h":
                    team = Team.objects.get(id=h)
                else:
                    team = Team.objects.get(id=a)

                events = PlayerEvent(id=int(event_id),
                                     match=match,
                                     date=new_date.replace(tzinfo=timezone.utc),
                                     player=player,
                                     team=team,
                                     time=time,
                                     event=event,
                                     home_away=home_away)
                events.save()
                events_added += 1

    return events_added

