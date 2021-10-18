import requests
import os


def get_song_url(song_name, artist_name):
    response = requests.get(
        "https://api.genius.com/search",
        headers={"Authorization": "Bearer " + os.getenv("genius_access_token")},
        params={"q": song_name + artist_name},
    )

    return response.json()["response"]["hits"][0]["result"]["url"]
