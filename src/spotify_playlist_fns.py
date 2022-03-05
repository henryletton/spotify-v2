'''
    File name: spotify_playlist_fns.py
    Author: Henry Letton
    Date created: 2021-02-06
    Python Version: 3.8.3
    Desciption: Functions that involve creation/editing spotify functions
'''

#%% Import modules
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import os
import numpy as np
from src.spotify_db_fns import sql_db_to_df, df_from_sql
import math

#%% Get df of my playlists
def get_my_playlists():
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="playlist-modify-public user-read-recently-played",
                                               show_dialog = True,
                                               open_browser = False))
    
    # Loop through 50 playlists at a time, adding to list
    playlist_list = []
    offset = 0
    total = 50
    
    while total > offset:
        my_playlists = sp.current_user_playlists(offset = offset)
        playlist_list += my_playlists['items']
        offset += 50
        total = my_playlists['total']
    
    # Convert list to df, keep required fileds, and output
    playlist_df = pd.DataFrame(playlist_list)
    return playlist_df[['id','name','description']]

#%% Get track ids from playlist id
def get_tracks_from_playlist_id(playlist_id):
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="playlist-modify-public user-read-recently-played",
                                               show_dialog = True,
                                               open_browser = False))
    
    # Loop through 50 playlists at a time, adding to list
    track_list = []
    offset = 0
    total = 100
    
    while total > offset:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset = offset)
        track_list += playlist_tracks['items']
        offset += 100
        total = playlist_tracks['total']
    
    # If no tracks then output empty df
    if track_list:
        # Convert list to df, keep required fileds, and output
        playlist_tracks_df = pd.DataFrame(track_list)
        playlist_tracks_df['id'] = [track['id'] for track in playlist_tracks_df['track']]
    else:
        playlist_tracks_df = pd.DataFrame(columns = ['id','added_at'])
    
    return playlist_tracks_df[['id','added_at']]


#%% Get playlist id from a playlist name
def get_playlist_id(playlist_name):
    #Get full list of playlist
    all_playlists = get_my_playlists()
    # Filter by name
    filter_playlists = all_playlists[all_playlists['name'] == playlist_name]
    # Only output if one playlist identified, can be created
    if len(filter_playlists.index) == 1:
        return filter_playlists['id'].item()
    
    elif len(filter_playlists.index) == 0:
        print('Playlist does not exist. Creating new playlist.')
        # Connect to my spotify app
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                                   client_secret=os.environ.get('spotify_client_secret'),
                                                   redirect_uri=os.environ.get('spotify_redirect_uri'),
                                                   scope="playlist-modify-public user-read-recently-played",
                                               show_dialog = True,
                                               open_browser = False))
        new_playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name)
        return new_playlist['id']
    
    elif len(filter_playlists.index) > 1:
        print('Playlist name is not unique')
        return

#%% Given track ids, update a playlist
def update_playlist(playlist_name,
                   track_ids,
                   update_type = "add_remove"):
    
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="playlist-modify-public user-read-recently-played",
                                               show_dialog = True,
                                               open_browser = False))
    
    # Use playlist name to get playlist and track ids
    playlist_id = get_playlist_id(playlist_name)
    playlist_tracks = get_tracks_from_playlist_id(playlist_id)
    playlist_track_ids = playlist_tracks['id']
    
    # From given tracks find those not in playlist and those not given
    new_ids = list(np.setdiff1d(track_ids,playlist_track_ids))
    old_ids = list(np.setdiff1d(playlist_track_ids,track_ids))
    
    # Loop through 100 ids at time, max api allows
    max_num_100s = math.ceil(max(len(new_ids),len(old_ids)) / 100)
    for chunk in range(max_num_100s):
        idx_start = chunk*100
        idx_end = (chunk+1)*100
        new_ids_chunk = new_ids[idx_start:idx_end]
        old_ids_chunk = old_ids[idx_start:idx_end]
    
        # Remove tracks not in given list, and add those not in playlist
        if update_type == "add_remove":
            if new_ids_chunk:
                sp.playlist_add_items(playlist_id, new_ids_chunk)
            if old_ids_chunk:
                sp.playlist_remove_all_occurrences_of_items(playlist_id, old_ids_chunk)
        
        # Only add new tracks
        elif update_type =="add_new" and new_ids_chunk:
            sp.playlist_add_items(playlist_id, new_ids_chunk)
    
    # Add new tracks maintaining order and keeping duplicates
    if update_type =="add_order":
        print('Need to code this up')
        for track_id in track_ids:
            sp.playlist_add_items(playlist_id, track_id)
        
    return

#%% Playlist accoding to total plays
def playlist_total_plays(engine,
                         playlist_name,
                         min_plays):
    
    # Connect to database
    engine.connect()
    
    # Get priority artist ids
    Music_Track_Plays = sql_db_to_df(engine = engine, 
                                       table_name = 'Music_Track_Plays')
    
    Music_Track_Plays = Music_Track_Plays[Music_Track_Plays['Plays'] >= min_plays]
    
    update_playlist(playlist_name, Music_Track_Plays['Track_Id'], "add_remove")
    
    return

#%% SQL query to update playlist
def sql_update_playlist(engine,
                        playlist_name,
                        sql_query,
                        update_type = "add_remove"):
    
    # Execute query
    query_df = df_from_sql(engine, sql_query)
    
    if 'Track_Id' not in query_df:
        print('Query did not return df with Track_Id')
        return
    
    # Use track_ids to update playlist
    update_playlist(playlist_name, query_df['Track_Id'], update_type)

    return

