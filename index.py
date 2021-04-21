import requests
import json
import os
from dotenv import load_dotenv

url = 'https://lichess.org/api/'
headers = None
gameId = ''

def initialize():
    load_dotenv()
    token = os.getenv('API_TOKEN')
    global headers 
    global gameId
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(f'{url}account/playing', headers=headers)
    gameId = json.loads(r.text)['nowPlaying'][0]['gameId']
    
    # when request fail (e.g invalid api token)
    if r.status_code != 200:
        print(f"status code: {r.status_code}, content: {r.content}")
        quit()


# move: starting, ending position (e.g. 'e2e4')
def move(move):
    return requests.post(f'{url}board/game/{gameId}/move/{move}', headers=headers)


if __name__ == "__main__":
    initialize()
    
    while True:
        mv = input("wpisz ruch: ")
        r = move(mv)
        
        if r.status_code != 200:
            print(f"status code: {r.status_code}, content: {r.content}")