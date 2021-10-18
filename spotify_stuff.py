import requests
import os
import random

def get_access_token():
    
    token_endpoint = 'https://accounts.spotify.com/api/token'

    token_params = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('spotify_client_id'),
        'client_secret': os.getenv('spotify_client_secret')
    }
    return requests.post(token_endpoint, token_params).json()['access_token']

# This function should be scrapped for m2
def artist_ids():
    mac_miller_id = '4LLpKhyESsyAXpc4laK94U'
    meek_mill_id = '20sxb77xiYeusSH8cVdatc'
    wiz_khalifa_id = '137W8MRPWKqSmrBGDBFSop'

    return [mac_miller_id, meek_mill_id, wiz_khalifa_id]

# This function should be scrapped for m2
def get_random_artist_id():
    random_index = random.randint(0,2)
    return artist_ids()[random_index]

def artistid_isvalid(artist_id):
    access_token = get_access_token()
    endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {
        'access_token': access_token,
        'market': 'US'
    }
    if not 'tracks' in requests.get(endpoint, headers).json():
        return False
    else:
        return True

def get_track(artist_id):
    access_token = get_access_token()


    endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {
        'access_token': access_token,
        'market': 'US'
    }

    tracks = requests.get(endpoint, headers).json()['tracks']
    track_index = random.randint(0,9)

    preview_url = tracks[track_index]['preview_url']
    track_name = tracks[track_index]['name']
    artist_name = tracks[track_index]['artists'][0]['name']
    img_url = tracks[track_index]['album']['images'][0]['url']

    return preview_url, track_name, artist_name, img_url


# This function will change for m2
def get_random_track():
    artist_id = get_random_artist_id()
    access_token = get_access_token()


    endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {
        'access_token': access_token,
        'market': 'US'
    }

    tracks = requests.get(endpoint, headers).json()['tracks']
    track_index = random.randint(0,9)

    preview_url = tracks[track_index]['preview_url']
    track_name = tracks[track_index]['name']
    artist_name = tracks[track_index]['artists'][0]['name']
    img_url = tracks[track_index]['album']['images'][0]['url']

    return preview_url, track_name, artist_name, img_url