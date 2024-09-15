import yaml, json
import spotipy
from spotipy import SpotifyOAuth
import requests
from geopy.geocoders import Nominatim
from country_mapping import country_map
import webbrowser

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Authentication - requires Spotify Developer credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['client_id'], client_secret=config['client_secret'],redirect_uri=config['redirect_uri']))

def get_geolocation():
    try:
        # Fetch the geolocation details using the IP-based API
        response = requests.get('https://ipinfo.io')
        data = response.json()
        country = data['country']
        print("Country: " + country)
        return country
    except Exception as e:
        print(f"Error fetching location from IP: {e}")
        return None


def get_featured_playlists_by_country(country_code):
    try:
        query = "Top 50 - " + country_map.get(country_code)
        playlist = sp.search(q=query, limit=1, type='playlist', market=country_code)
        playlist_data = playlist.get('playlists').get('items')
        playlist_url = playlist_data[0].get('external_urls').get('spotify')

        webbrowser.open(playlist_url)

    except spotipy.SpotifyException as e:
        raise SpotifyError(f"Spotify API error: {e}")


if __name__=="__main__":
    user_input = input("Would you like to use your geolocation to get recommendations? (e.g., y/n) ")
    if user_input == 'y':
        try:
            country = get_geolocation()
        except GeoLocationError as ge:
            print(f"Failed to get geolocation: {ge}")
    elif user_input == 'n':
        country = input("Enter the destination country code (e.g., US, GB, IT): ").strip().upper()
    else: 
        raise ValueError("input must be y/n")
    
    if country:
        get_featured_playlists_by_country(country)

