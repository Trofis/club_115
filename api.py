import requests
import datetime
import json

#doc : https://www.api-football.com/documentation

# API Auth
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "28690fa489mshd60bc899567836fp17400ejsnf7f16b7f5883"
    }
# Static data 
f = open('data_clubs.json')
data_clubs = json.load(f)
# Get current season year
current_year = datetime.datetime.now().year if datetime.datetime.now().month > 7 else datetime.datetime.now().year-1

# Get leagues infos
# ['name', 'id', 'season', 'country']
leagues = requests.get("https://api-football-v1.p.rapidapi.com/v2/leagues/season/{}".format(current_year), headers=headers).json()
leagues = [[league['name'], league['league_id'], league['season'], league['country']] for league in leagues["api"]["leagues"] if league['name'] in data_clubs['leagues'] and data_clubs['leagues'][league['name']] == league['country'] and league['season'] == current_year]

# Get next round & next matches
# { 'country' : ['id', 'event_date', 'round', ['team_id', 'team_name', 'logo'], ['team_id', 'team_name', 'logo']]}
coming_play_off_per_country = {}
for league in leagues:
    coming_round = requests.get("https://api-football-v1.p.rapidapi.com/v2/fixtures/rounds/{}/current".format(league[1]), headers=headers).json()['api']['fixtures'][0]
    print(league[1], coming_round)
    coming_play_off = requests.get("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{}/{}".format(league[1], coming_round), headers=headers).json()['api']['fixtures']
    coming_play_off = [[play_off['fixture_id'], play_off['event_date'], play_off['round'], [play_off['homeTeam']['team_id'], play_off['homeTeam']['team_name'], play_off['homeTeam']['logo']], [play_off['awayTeam']['team_id'], play_off['awayTeam']['team_name'], play_off['awayTeam']['logo']] ] for play_off in coming_play_off ]
    coming_play_off_per_country[league[3]] = coming_play_off

print(coming_play_off_per_country)
# Get next match
