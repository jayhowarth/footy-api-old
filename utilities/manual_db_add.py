from footy_api.models import Competition, Country, Federation, Team

def add_competition():
    #country_id = 22
    #country = Country.objects.get(id=country_id)

    competitions = Competition(id=int("0"),
                               name="Unknown",
                               country=None,
                               federation=None)
    competitions.save()
    return "Added 0"


def add_team():
    #country_id = 22
    #country = Country.objects.get(id=country_id)

    teams = Team(id=int(0),
                 name="Unknown",
                 stadium="Unknown",
                 country=None,
                 country_is_real=0,
                 federation=None)
    teams.save()
    return "Added 0"