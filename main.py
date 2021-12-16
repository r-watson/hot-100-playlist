import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

load_dotenv(r"C:\Users\watsorob\Google Drive\Programming\Python\EnvironmentVariables\.env.txt")
SPOTIPY_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SCOPE = "playlist-modify-private"
REDIRECT_URI = "http://example.com"

# year = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = "2000-06-02"
year_split = year.split("-")[0]
web_file = f"./data/{year}-top100.txt"
webpage_url = f"https://www.billboard.com/charts/hot-100/{year}/"

# auth_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(auth_manager=auth_manager)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI))
user_id = sp.current_user()['id']

def get_web_page():
    # scrape HTML from page
    result = requests.get(webpage_url)
    # convert HTML to text
    result_html = result.text
    with open(web_file, mode='w', encoding='utf-8') as page:
        page.write(result_html)

def read_web_file():

    try:
        open(web_file)
    except FileNotFoundError:
        get_web_page()
    finally:
        # Read the web page from the file
        with open(web_file, mode='r', encoding='utf-8') as page:
            content = page.read()
    soup = BeautifulSoup(content, 'html.parser')
    song_title = soup.select("li ul li h3")
    song_names = [song.getText().strip("\n") for song in song_title]
    # for song in song_names:
    #     print(song)

    playlist_id = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
    playlist_uri = playlist_id['uri']

    # search = sp.search(q=f"track:{song_names[1]} year:{year_split} ", type='track', limit=1)
    # song_uri = search['tracks']['items'][0]['artists'][0]['uri']
    song_uri = []

    for song in song_names:
        # get song URIs from spotify and add to playlist
        search = sp.search(q=f"track:{song} year:{year_split} ", type='track', limit=1)
        # pprint(search)
        try:
            # uri = search['tracks']['items'][0]['artists'][0]['uri']
            uri = search['tracks']['items'][0]['uri']
            song_uri.append(uri)
        except IndexError:
            print(f"{song} does not exist in Spotify. Skipped.")
    print(song_uri)

    sp.playlist_add_items(playlist_id=playlist_uri, items=song_uri)


# Read web file if it exists. Load from Internet if it does not.
read_web_file()
