import requests
import json
import os
from dotenv import load_dotenv

url = 'https://lichess.org'
gameId = ''
token = ''

headers = {    
    'Authorization': '',
    'Accept': 'application/json'
}

def initialize():
    load_dotenv()
    global token
    token = os.getenv('API_TOKEN')
    headers['Authorization'] = f'Bearer {token}'

    r = requests.get(f'{url}/api/account', headers=headers) # authorization test request

    # when request fail (e.g invalid api token)
    if r.status_code != 200:
        print(f"initializa() status code: {r.status_code}, content: {r.content}")
        quit()


# move: starting, ending position (e.g. 'e2e4')
def move(move):
    return requests.post(f'{url}/api/board/game/{gameId}/move/{move}', headers=headers)


def chooseGame():
    gamesId = []
    r = requests.get(f'{url}/api/account/playing', headers=headers)
    i = 1

    for game in json.loads(r.text)['nowPlaying']:
        gamesId.append(game['gameId'])
        opponent = game['opponent']
        print(f"{i}. opponent: {opponent['username']}({opponent.get('ia', opponent.get('rating'))}), color: {game['color']}, last move: {game['lastMove']}")
        i = i + 1
    
    choice = input("choose game: ")
    global gameId
    gameId = gamesId[int(choice) - 1]

if __name__ == "__main__":
    initialize()
    chooseGame()

    while True:
        mv = input("Type move: ")
        r = move(mv)
        
        if r.status_code != 200:
            print(f"status code: {r.status_code}, content: {r.content}")