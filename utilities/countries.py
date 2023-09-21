import json
from utilities.api_manager import APIManager as api
from utilities import mongo as mg


def update_countries():
    url = "https://api-football-v1.p.rapidapi.com/v3/countries"
    querystring = {}
    response = api.get_request(url, querystring)
    json_response = json.loads(response)
    total_countries = json_response['results']
    all_countries = json_response['response']
    no_added = 0
    for x in all_countries:
        country_name = x['name']
        country_code = x['code']
        country_flag = x['flag']

        country = {
            "name": country_name,
            "code": country_code,
            "flag": country_flag
        }
        if mg.count_documents("countries", {"name": country_name}) == 0:
            mg.add_record("countries", country)
            no_added += 1

    return f'{no_added} Countries'


