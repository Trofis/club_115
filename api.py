import requests
import datetime
import json

# doc : https://www.api-football.com/documentation

# TO DO :
#   - Get names teams from a particular league --> go find image []
#   - Get next round league --> Generate calendar [x]
#   - Get leagues infos []

# API Auth
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "28690fa489mshd60bc899567836fp17400ejsnf7f16b7f5883"
}
# Static data
f = open('data_clubs.json')
data_clubs = json.load(f)

# Get current season year
current_year = datetime.datetime.now().year if datetime.datetime.now(
).month > 7 else datetime.datetime.now().year-1

# Get leagues infos
# ['name', 'id', 'season', 'country']


def get_leagues_infos():
    print("############## GET LEAGUES INFOS ################")
    # Get leagues
    leagues = requests.get(
        "https://api-football-v1.p.rapidapi.com/v2/leagues/season/{}".format(current_year), headers=headers).json()

    JSON_leagues = {}
    for league in leagues["api"]["leagues"]:
        if league['name'] in data_clubs['leagues'] and data_clubs['leagues'][league['name']] == league['country'] and league['season'] == current_year:
            JSON_leagues[league['country']] = {
                "league_id": league["league_id"],
                "league_name": league['name'],
                "league_season": league["season"],
                "league_teams": []
            }
    # Get teams
    count = 0
    for infos in JSON_leagues.items():
        print(infos)
        infos[1]["league_teams"] = (requests.get(
            "https://api-football-v1.p.rapidapi.com/v2/teams/league/{}".format(
                infos[1]["league_id"]),
            headers=headers).json()["api"]["teams"])

        count += 1

    # Write JSON
    with open("leaugues_infos.json", "w") as write_file:
        json.dump(JSON_leagues,
                  write_file, indent=4, sort_keys=True)


def get_next_leagues_round():
    print("############## GET NEXT LEAGUES ROUND ################")

    with open("leaugues_infos.json", "r") as read_file:
        leagues = json.load(read_file)

    # Get next round & next matches
    # { 'country' : ['id', 'event_date', 'round', ['team_id', 'team_name', 'logo'], ['team_id', 'team_name', 'logo']]}
    coming_play_off_per_country = {}
    print(leagues)
    for league in leagues.items():
        coming_round = requests.get("https://api-football-v1.p.rapidapi.com/v2/fixtures/rounds/{}/current".format(
            league[1]["league_id"]), headers=headers).json()['api']['fixtures'][0]
        print(league[1], coming_round)
        coming_play_off = requests.get("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{}/{}".format(
            league[1]["league_id"], coming_round), headers=headers).json()['api']['fixtures']
        coming_play_off = [[play_off['fixture_id'], play_off['event_date'], play_off['round'], [play_off['homeTeam']['team_id'], play_off['homeTeam']['team_name'],
                                                                                                play_off['homeTeam']['logo']], [play_off['awayTeam']['team_id'], play_off['awayTeam']['team_name'], play_off['awayTeam']['logo']]] for play_off in coming_play_off]
        coming_play_off_per_country[league[0]] = coming_play_off

    with open("coming_rounds.json", "w") as write_file:
        json.dump(coming_play_off_per_country,
                  write_file, indent=4, sort_keys=True)


# get_leagues_infos()
get_next_leagues_round()

# Get next match
