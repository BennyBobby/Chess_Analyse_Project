import requests
import json
import time
import os
USER_AGENT= "Mozilla/5.0 (compatible; Chess_Analyse/1.0; +https://chess.com)"

def make_request(url:str):
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error request with {url} which is {err}")
        return None
    
def get_chess_data(username: str):
    url=f"https://api.chess.com/pub/player/{username}/games/archives"
    data=make_request(url)
    if data and "archives" in data: #we check if data is not empty and archives key is in data
        return data["archives"]
    return []

def save_games_to_json(username: str, month:int, year:int, games_data:list):
    user_json_dir = os.path.join("data/json", username)
    os.makedirs(user_json_dir, exist_ok=True) #we create the user folder in data/json
    filename = os.path.join(user_json_dir, f"{username}_{year}_{month}.json")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(games_data, f, ensure_ascii=False, indent=4)
    except IOError as err:
        print(f"Error {err} during saving file: {filename}")

def download_monthly_games(archive_url: str):
    print(f"Downloading games from: {archive_url}")
    data = make_request(archive_url)
    if data and "games" in data:
        return data["games"]
    return []
### function that extracts just the last 12 months 
# def extract_chess_player_data(username:str, number_month:int=12):
#     print(f"=>Start of the extraction data of {username}")
#     archives=get_chess_data(username)
#     if not archives:
#         print(f"No data found with {username}, play chess then")
#         return 0
#     total_games_downloaded = 0

#     for i, archive_url in enumerate(archives[-number_month:]):
#         parts = archive_url.split('/')
#         year = int(parts[-2])
#         month = int(parts[-1])
#         games = download_monthly_games(archive_url)
#         if games: 
#             save_games_to_json(username, year, month, games)
#             total_games_downloaded+=len(games)
#         time.sleep(1)
#     print(f"=>Extraction done. {total_games_downloaded} games for {username}")
def extract_chess_player_data(username:str):
    print(f"=>Start of the extraction data of {username}")
    archives=get_chess_data(username)
    if not archives:
        print(f"No data found with {username}, play chess then")
        return 0
    total_games_downloaded = 0

    for i, archive_url in enumerate(archives):
        parts = archive_url.split('/')
        year = int(parts[-2])
        month = int(parts[-1])
        games = download_monthly_games(archive_url)
        if games: 
            save_games_to_json(username, year, month, games)
            total_games_downloaded+=len(games)
        time.sleep(1)
    print(f"=>Extraction done. {total_games_downloaded} games for {username}")

if __name__ == "__main__":
    test_username = input("Which username do you want to extract data of? ")
    extract_chess_player_data(test_username)
