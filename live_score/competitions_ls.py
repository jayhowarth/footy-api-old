from footy_api import serializers
import requests
from footy_api.models import Competition, Country, Federation
from footy_api.serializers import CompetitionsSerializer, CountriesSerializer
from footy import config

url = "https://livescore-api.com/api-client/competitions/list.json"
live_scores_url = url + "?" + config.live_scores_auth


def update_competitions():
    response = requests.get(live_scores_url)
    json_response = response.json()
    total = len(json_response['data']['competition']) - 1
    no_added = 0
    for x in range(0, total):
        comp_id = json_response['data']['competition'][x]['id']
        comp_name = json_response['data']['competition'][x]['name']
        if len(json_response['data']['competition'][x]['countries']) > 0:
            country_id = json_response['data']['competition'][x]['countries'][0]['id']
            country = Country.objects.get(id=country_id)
        else:
            country = None
        if len(json_response['data']['competition'][x]['federations']) > 0:
            federation_id = json_response['data']['competition'][x]['federations'][0]['id']
            federation = Federation.objects.get(id=federation_id)
        else:
            federation = None

        exists = Competition.objects.filter(id=comp_id).exists()
        if not exists:
            competitions = Competition(id=int(comp_id),
                                       name=comp_name,
                                       country=country,
                                       federation=federation)
            competitions.save()
            no_added += 1

    return f'{no_added} Competitions'


def get_competition_name(comp_id):
    competition = Competition.objects.get(id=comp_id)
    comp_serializer = CompetitionsSerializer(competition)
    try:
        country = Country.objects.get(id=comp_serializer.data['country'])
    except:
        return ""
    country_serializer = CountriesSerializer(country)
    comp_name = country_serializer.data['name'] + ' - ' + comp_serializer.data['name']
    return comp_name
