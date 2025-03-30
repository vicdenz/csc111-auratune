import time
import requests
import re

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.expiry_time = 0
    
    def auth(self):
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(token_url, data=token_data, headers=token_headers)
        token_data = response.json()

        self.access_token = token_data.get('access_token')
        self.expiry_time = time.time() + token_data.get('expires_in')  # in seconds

    def get_valid_token(self):
        if not self.access_token or (time.time() - 5) > self.expiry_time:
            self.auth()

    def get_tracks_by_genre(self, genre, num_tracks=100):
        self.get_valid_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }
        tracks_found = []
        limit = 50 # Maximum allowed by Spotify API

        remaining_tracks = num_tracks
        offset = 0
        while remaining_tracks > 0:
            search_url = f'https://api.spotify.com/v1/search?q=genre:"{genre}"&type=track&limit={limit}&offset={offset}'
            response = requests.get(search_url, headers=headers)
            
            if response.status_code != 200:
                print(f"Error: {response}")
                return None
            search_data = response.json()
            tracks = search_data.get("tracks").get("items")

            for i in range(0, min(remaining_tracks, limit)):
                tracks_found.append(tracks[i].get("id"))

            remaining_tracks -= limit
            offset += limit

        return tracks_found

    def get_track_features(self, track_id): # API ENDPOINT REMOVED
        self.get_valid_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
        response = requests.get(audio_features_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response}")
            return None

    def get_several_track_features(self, track_ids): # API ENDPOINT REMOVED
        
        tracks_features = []
        for track_id in track_ids:
            tracks_features.append(self.get_track_features(track_id))

        return tracks_features

    def get_artist(self, artist_id):
        self.get_valid_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
        response = requests.get(artist_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response}")
            return None

    def get_several_artists(self, artist_ids):
        self.get_valid_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        artist_url = f'https://api.spotify.com/v1/artists/?ids={",".join(artist_ids[0:50])}'
        response = requests.get(artist_url, headers=headers)

        if response.status_code == 200:
            return response.json().get('artists')
        else:
            print(f"Error: {response}")
            return None

    def get_artist_id(self, artist_name):
        self.get_valid_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        search_url = "https://api.spotify.com/v1/search"
        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1  # Get only the top result
        }

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            artists = data.get('artists', {}).get('items', [])
            if artists:
                return artists[0]['id']  # Return the first artist's ID
            else:
                return []
        else:
            print(f"Error: {response}")
            return None


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from api import SpotifyAPI

    # Load environment variables
    load_dotenv()

    # Spotify API credentials
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    # Create an instance of SpotifyAPI
    spotify_api = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)

    # Get a valid token
    spotify_api.get_valid_token()

    artists = ['Avicii', 'Aphex Twin', 'Deftones', 'Michael Jackson', 'Daddy Yankee']
    artist_ids = [spotify_api.get_artist_id(artist) for artist in artists]
    for artist in spotify_api.get_several_artists(artist_ids):
        print(f"{artist['name']}: {artist['genres']}")