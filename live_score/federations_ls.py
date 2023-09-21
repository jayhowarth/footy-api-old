import requests
from footy_api.models import Federation
from footy import config


def update_federations():
    url = "http://livescore-api.com/api-client/federations/list.json"
    live_scores_url = url + "?" + config.live_scores_auth
    response = requests.get(live_scores_url)
    json_response = response.json()
    total = len(json_response['data']['federation'])
    no_added = 0
    for x in range(0, total):
        federation_id = json_response['data']['federation'][x]['id']
        federation_name = json_response['data']['federation'][x]['name']

        exists = Federation.objects.filter(id=federation_id).exists()
        if not exists:
            federation = Federation(id=int(federation_id),
                                    name=federation_name)
            federation.save()
            no_added += 1

    return (f"{no_added} Federations")