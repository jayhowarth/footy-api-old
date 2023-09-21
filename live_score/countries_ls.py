import requests
from footy_api.models import Country, NationalTeam, Federation
from footy import config


def update_countries():
    url = "https://livescore-api.com/api-client/countries/list.json"
    live_scores_url = url + "?" + config.live_scores_auth
    response = requests.get(live_scores_url)
    json_response = response.json()
    total = len(json_response['data']['country'])
    no_added = 0
    for x in range(0, total):
        country_id = json_response['data']['country'][x]['id']
        country_name = json_response['data']['country'][x]['name']
        is_country = json_response['data']['country'][x]['is_real']
        if (json_response['data']['country'][x]['national_team']) is not None:
            national_team_id = json_response['data']['country'][x]['national_team']['id']
            national_team_name = json_response['data']['country'][x]['national_team']['name']
            national_team_stadium = json_response['data']['country'][x]['national_team']['stadium']
            national_team_location = json_response['data']['country'][x]['national_team']['location']

            add_national_team(national_team_id, national_team_name, national_team_stadium, national_team_location)

        else:
            national_team_id = None

        
        if json_response['data']['country'][x]['federation'] is not None:
            federation_id = int(json_response['data']['country'][x]['federation']['id'])
            federation = Federation.objects.get(id=federation_id)
        else:
            federation = None

        
        if json_response['data']['country'][x]['national_team'] is not None:
            national_team_id = json_response['data']['country'][x]['national_team']['id']
            national_team = NationalTeam.objects.get(id=national_team_id)
        else:
            national_team = None

        all_leagues_link = json_response['data']['country'][x]['leagues']
        all_scores_link = json_response['data']['country'][x]['scores']

        exists = Country.objects.filter(id=country_id).exists()
        if not exists:
            countries = Country(id=int(country_id),
                                name=country_name,
                                is_country=is_country,
                                national_team=national_team,
                                federation=federation,
                                all_leagues_link=all_leagues_link,
                                all_scores_link=all_scores_link)
            countries.save()
            no_added += 1
    return (f'{no_added} Countries')

def add_national_team(nt_id, nt_name, nt_stadium, nt_location):
    exists = NationalTeam.objects.filter(id=nt_id).exists()
    if not exists:
        national_team = NationalTeam(id=int(nt_id),
                                     name=nt_name,
                                     stadium=nt_stadium,
                                     location=nt_location)
        national_team.save()
        return ("Added National Team")
    else:
        return ("National Team Exists")

