from django.contrib import admin
from django.urls import path
from footy_api import views

urlpatterns = [
    path('api/v1/update_all', views.main_update),
    path('api/v1/get_countries', views.get_countries),
    path('api/v1/update_today', views.update_todays_fixtures),
    #path('api/v1/update_today_league/<int:league_id>', views.update_todays_fixtures_for_league),
    path('api/v1/get_leagues', views.get_leagues),
    path('api/v1/update_leagues', views.update_league_standings),
    # path('api/v1/get_competitions', views.get_competitions),
    # # path('api/v1/get_federations', views.get_federations),
    # path('api/v1/update_standings/<int:competition_id>', views.get_standings),
    path('api/v1/update_all_standings', views.get_all_standings),
    path('api/v1/update_fixtures_for_league', views.update_all_fixtures_for_league),
    path('api/v1/get_teams', views.get_teams),
    path('api/v1/update_matches/<int:team_id>', views.get_matches),
    path('api/v1/get_fixtures', views.get_todays_fixtures),
    path('api/v1/get_fixtures_date', views.get_fixtures_by_date),
    path('api/v1/get_results_date', views.get_results_by_date),
    path('api/v1/manual_add', views.add_manually),
    path('api/v1/get_team_stats/<int:team_id>', views.get_team_statistics),
    path('api/v1/test', views.test),
    path('api/v1/dummy', views.dummy),
    path('api/v1/stats', views.stats),
]