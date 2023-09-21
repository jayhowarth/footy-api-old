import requests
from footy_api.models import Team, Country, Federation
from footy import config


def update_teams():
    url = "https://livescore-api.com/api-client/teams/list.json"
    live_scores_url = url + "?" + config.live_scores_auth
    results_per_page = '100'
    response = requests.get(live_scores_url, params={"size": results_per_page})
    json_response = response.json()
    pages = json_response['data']['pages']
    total = json_response['data']['total']
    results_per_page = '100'
    page_no = 1
    no_added = 0
    #for p in range(1, pages):
    while page_no < pages + 1:
        querystring = {"size": results_per_page, "page": page_no}
        response = requests.get(live_scores_url, params=querystring)
        json_response = response.json()
        page_no += 1
        results_on_page = len(json_response['data']['teams'])
        for x in range(0, int(results_on_page)):
            team_id = json_response['data']['teams'][x]['id']
            team_name = json_response['data']['teams'][x]['name']
            stadium = json_response['data']['teams'][x]['stadium']
            if len(json_response['data']['teams'][x]['country']) > 0:
                country_id = json_response['data']['teams'][x]['country']['id']
                country = Country.objects.get(id=country_id)
                country_is_real = json_response['data']['teams'][x]['country']['is_real']
            else:
                country = None
            if len(json_response['data']['teams'][x]['federation']) > 0:
                federation_id = json_response['data']['teams'][x]['federation']['id']
                federation = Federation.objects.get(id=federation_id)
            else:
                federation = None
            exists = Team.objects.filter(id=team_id).exists()
            if not exists:
                teams = Team(id=int(team_id),
                            name=team_name,
                            stadium=stadium,
                            country=country,
                            country_is_real=country_is_real,
                            federation=federation)
                teams.save()
                no_added += 1

    return f'{no_added} Teams'
