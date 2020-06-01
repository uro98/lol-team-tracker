import requests
import time

summoner_name = 'Joppiesaus'
region = 'euw1'
api_key = 'RGAPI-c81d321a-e0c0-4e0b-87d0-23f00ce14576'
account_id = None
last_timestamp = None
rate_limit = 1.201

def get(url):
    response = requests.get(url)
    json_response = response.json()
    time.sleep(rate_limit)
    return json_response

def process_player(player):
    summoner_id = player['player']['summonerId']
    summoner_name = player['player']['summonerName']

    leagues = get(f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
    
    for league in leagues:
        if league['queueType'] == 'RANKED_SOLO_5x5':
            tier = league['tier']
            rank = league['rank']
            lp = league['leaguePoints']
            print(f'{summoner_name}: {tier} {rank} {lp}lp')

def process_match(match):
    game_id = match['gameId']
    match_details = get(f'https://{region}.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api_key}')
    
    players = match_details['participantIdentities']
    for player in players:
        process_player(player)

def process_last_hundred_games():
    matchlist = get(f'https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key}')
    matches = matchlist['matches']
    for match in matches:
        process_match(match)

def main():
    if last_timestamp:
        print('')
    else:
        summoner = get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}')
        account_id = summoner['accountId']
        process_last_hundred_games()

if __name__ == '__main__':
    main()