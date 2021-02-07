'''
    File name: test_spotipy.py
    Author: Henry Letton
    Date created: 2021-01-10
    Python Version: 3.8.3
    Desciption: Test python spotify library
'''

#%% Import modules
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
#import mysql.connector
from sqlalchemy import create_engine 
import os
from urllib.error import HTTPError

#%% Load system variables from .env file
from dotenv import load_dotenv
os.chdir('C:\\Users\\henry\\OneDrive\\Documents\\Python\\spotify-v2')
load_dotenv()

#%% Get recently played from spotify api

# Connect to my spotify app
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="playlist-modify-public",
                                               show_dialog = True,
                                               open_browser = False))
                                               #scope="user-read-recently-played"))

#%% Test reading
db_url = f'mysql+mysqlconnector://{os.environ.get("sql_user")}:{os.environ.get("sql_pw")}@{os.environ.get("sql_db")}'
engine = create_engine(db_url)

sql_artists = pd.read_sql_query('SELECT * FROM Music_Refresh_Artist', engine)
sql_albums = pd.read_sql_query('SELECT * FROM Music_Refresh_Album', engine)
sql_tracks = pd.read_sql_query('SELECT * FROM Music_Refresh_Track', engine)

# Limit to specfic country, only artist albums?
try:
    artist_details = sp.artist("afgsdgsdfhfghfgh")
except HTTPError and spotipy.SpotifyException:
    print("Error")
except:
    print("Other Error")
    
    
artist_details2 = sp.artist_albums(sql_artists['Artist_Id'][0], limit=50) #Will need offset to get all
album_details = sp.album('01WEcEzoa9mfh8fIDhvV1M')
album_track_details = sp.album_tracks(sql_albums['Album_Id'][0], market="GB")
track_details = sp.track(sql_tracks['Track_Id'][0]) #Multiple tracks at once
track_details2 = sp.audio_analysis(sql_tracks['Track_Id'][0]) #Not this one
track_details3 = sp.audio_features(sql_tracks['Track_Id'][0]) #Multiple?

artist_genres_df = pd.DataFrame({'Genre' : artist_details['genres']})
artist_genres_df['Id'] = artist_details['id']

#%% user info
sp.current_user()

#%% Playlist

my_playlists = sp.current_user_playlists()
specific_playlist = sp.playlist('1dNTdytn74c4m2ryYeNOMD')
specific_playlist_tracks = sp.playlist_tracks('1dNTdytn74c4m2ryYeNOMD', offset = 100)
#playlist_add_items, playlist_remove_all_occurrences_of_items
test0 = sp.user_playlist_create(sp.current_user()['id'], 'Test')


