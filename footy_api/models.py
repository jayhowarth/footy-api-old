from django.db import models


class NationalTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    stadium = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Federation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LSCountry(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    national_team = models.ForeignKey(NationalTeam, on_delete=models.CASCADE, null=True)
    is_country = models.BooleanField(blank=True, null=True)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE, null=True)
    all_leagues_link = models.CharField(max_length=255, blank=True, null=True)
    all_scores_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, blank=True, null=True)
    flag = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


#
# class League(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=100)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
#     live_score_url = models.CharField(max_length=200, blank=True, null=True)
#
#     def __str__(self):
#         return self.name


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    stadium = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    country_is_real = models.CharField(max_length=5, blank=True, null=True)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class LeagueStandings(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    league_id = models.CharField(max_length=10)
    season_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=10)
    points = models.CharField(max_length=10)
    matches = models.CharField(max_length=10)
    goal_diff = models.CharField(max_length=10)
    goals_scored = models.CharField(max_length=10)
    goals_conceded = models.CharField(max_length=10)
    lost = models.CharField(max_length=10)
    drawn = models.CharField(max_length=10)
    won = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LeagueStandingsJson(models.Model):
    id = models.IntegerField(primary_key=True)
    season_id = models.CharField(max_length=10)
    league_name = models.CharField(max_length=100)
    league_table = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.league_name


class AllMatches(models.Model):
    id = models.IntegerField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.CASCADE, null=True)
    away_team = models.ForeignKey(Team, related_name="away_team", on_delete=models.CASCADE, null=True)
    score = models.CharField(max_length=10)
    ht_score = models.CharField(max_length=10, blank=True)
    ft_score = models.CharField(max_length=10)
    et_score = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.id


class PlayerEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    match = models.ForeignKey(AllMatches, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    player = models.CharField(max_length=100)
    event = models.CharField(max_length=20)
    time = models.CharField(max_length=5)
    home_away = models.CharField(max_length=5)

