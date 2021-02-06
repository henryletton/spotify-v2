'''
    File name: spotify_api_fns.py
    Author: Henry Letton
    Date created: 2021-01-20
    Python Version: 3.8.3
    Desciption: Functions that interact with the Spotify API
'''

#%% Import modules
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import os
from urllib.error import HTTPError

#%% Load system variables from .env file
from dotenv import load_dotenv
load_dotenv()

#%% Get recently played information as dataframes in dictionayy
def get_recently_played_df():
    
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                                   client_secret=os.environ.get('spotify_client_secret'),
                                                   redirect_uri=os.environ.get('spotify_redirect_uri'),
                                                   scope="user-read-recently-played"))
    
    # Get recently played
    rec_played = sp.current_user_recently_played()
    rec_played_df = pd.DataFrame(rec_played['items'])
    
    # Tidy data into tracks data frame
    rec_tracks = rec_played_df.rename(columns={"played_at": "DateTime"})[['DateTime']]
    rec_tracks['Track_Name'] = [track['name'] for track in rec_played_df['track']]
    rec_tracks['Track_Id'] = [track['id'] for track in rec_played_df['track']]
    rec_tracks['Plays'] = 1
    rec_tracks['Skips'] = 0
    rec_tracks['Source'] = 'Spotify'
    
    # Get albums
    album_id_list = [track['album']['id'] for track in rec_played_df['track']]
    rec_albums = pd.DataFrame({'Album_Id' : list(set(album_id_list))})
    
    # Get Artists
    artist_id_list = [artist['id'] for track in rec_played_df['track'] for artist in track['artists']]
    rec_artists = pd.DataFrame({'Artist_Id' : list(set(artist_id_list))})
    
    # Get track album mapping
    map_tr_al = pd.DataFrame({'Album_Id' : album_id_list,
                              'Track_Id' : [track['id'] for track in rec_played_df['track']]})
    
    # Get track artist mapping
    map_tr_ar = pd.DataFrame({'Artist_Id' : artist_id_list,
                              'Track_Id' : [track['id'] for track in rec_played_df['track'] for artist in track['artists']]})
    
    # Get album artist mapping
    map_al_ar = pd.DataFrame({'Album_Id' : [track['album']['id'] for track in rec_played_df['track'] for artist in track['artists']],
                              'Artist_Id' : artist_id_list})
    
    # Store in dictionary
    rp_df_dict = {"rec_tracks" : rec_tracks,
               "rec_albums" : rec_albums,
               "rec_artists" : rec_artists,
               "map_tr_al" : map_tr_al,
               "map_tr_ar" : map_tr_ar,
               "map_al_ar" : map_al_ar}

    return rp_df_dict

#%% Get artist information
def get_artist_info(artist_id,
                  get_albums = True):
    
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="user-read-recently-played"))
    
    # Get artist details and catch errors
    art_id_df = pd.DataFrame({'Artist_Id' : [artist_id]})
    empty_df =  pd.DataFrame(columns = ['Artist_Id'])
    try:
        artist_details = sp.artist(artist_id)
        ar_df_dict = {'removed' : empty_df,
                      'error' : empty_df}
    except HTTPError and spotipy.SpotifyException:
        print("Artist does not exist. Assume removed from spotify")
        ar_df_dict = {'removed' : art_id_df,
                      'error' : art_id_df}
        return ar_df_dict
    except:
        print("Other issue. ")
        ar_df_dict = {'removed' : empty_df,
                      'error' : art_id_df}
        return ar_df_dict
    
    # Store in df
    artist_details_df = pd.DataFrame({'Artist_Id' : [artist_details['id']],
                                      'Artist_Name' : [artist_details['name']],
                                      'Artist_Popularity' : [artist_details['popularity']],
                                      'Total_Followers' : [artist_details['followers']['total']]})
    
    # Store in dictionary
    ar_df_dict["artist_details_df"] = artist_details_df
    
    # Get artist genre details in df
    if "genres" in artist_details:
        if artist_details['genres']:
            artist_genres_df = pd.DataFrame({'Genre' : artist_details['genres']})
            artist_genres_df['Id'] = artist_details['id']
            artist_genres_df['Type'] = 'Artist'
            
            # Add to dictionary
            ar_df_dict['artist_genres_df'] = artist_genres_df
    
    # Default to get album ids for artist
    if get_albums:
        # Loop through artist albums 50 at a time until complete list of album ids
        num_albums = 100
        offset = 0
        album_ids = []
        
        while num_albums > offset:
            artist_details2 = sp.artist_albums(artist_id, limit=50, country="GB", offset=offset)
            num_albums = artist_details2['total']
            if artist_details2['items']:
                album_ids += list(pd.DataFrame(artist_details2['items'])['id'])
            offset += 50
        
        # Album id list as datatframe
        album_ids_df = pd.DataFrame({'Album_Id' : album_ids})
    
        # Add in dictionary
        ar_df_dict['album_ids_df'] = album_ids_df
        
        # Also get artist to album mapping df
        map_al_ar = album_ids_df.copy()
        map_al_ar['Artist_Id'] = artist_details['id']
        
        # Add in dictionary
        ar_df_dict['map_al_ar'] = map_al_ar
    
    return ar_df_dict

#%% Get album information
def get_album_info(album_id,
                   get_tracks = True):
    
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="user-read-recently-played"))
    
    # Get album details and catch errors
    alb_id_df = pd.DataFrame({'Album_Id' : [album_id]})
    empty_df =  pd.DataFrame(columns = ['Album_Id'])
    try:
        album_details = sp.album(album_id)
        al_df_dict = {'removed' : empty_df,
                      'error' : empty_df}
    except HTTPError and spotipy.SpotifyException:
        print("Album does not exist. Assume removed from spotify")
        al_df_dict = {'removed' : alb_id_df,
                      'error' : alb_id_df}
        return al_df_dict
    except:
        print("Other issue. ")
        al_df_dict = {'removed' : empty_df,
                      'error' : alb_id_df}
        return al_df_dict
    
    # Store in df
    album_details_df = pd.DataFrame({'Album_Id' : [album_details['id']],
                                      'Album_Name' : [album_details['name']],
                                      'Release_Date' : (album_details['release_date']+'-01-01')[0:10],
                                      'Total_Tracks' : [album_details['total_tracks']],
                                      'Album_Type' : [album_details['album_type']],
                                      'Label' : [album_details['label']],
                                      'UPC' : [album_details['external_ids']['upc']]})
    
    # Store in dictionary
    al_df_dict["album_details_df"] = album_details_df
    
    # Get album genre details in df
    if "genres" in album_details:
        if album_details['genres']:
            album_genres_df = pd.DataFrame({'Genre' : album_details['genres']})
            album_genres_df['Id'] = album_details['id']
            album_genres_df['Type'] = 'Album'
            
            # Add to dictionary
            al_df_dict['album_genres_df'] = album_genres_df
    
    # Default to get track ids for album
    if get_tracks:
        # Loop through artist albums 50 at a time until complete list of album ids
        num_albums = 100
        offset = 0
        track_ids = []
        
        while num_albums > offset:
            album_details2 = sp.album_tracks(album_id, limit=50, market="GB", offset=offset)
            num_albums = album_details2['total']
            if album_details2['items']:
                track_ids += list(pd.DataFrame(album_details2['items'])['id'])
            offset += 50
        
        # Album id list as datatframe
        track_ids_df = pd.DataFrame({'Track_Id' : track_ids})
    
        # Add in dictionary
        al_df_dict['track_ids_df'] = track_ids_df
        
        # Also get artist to album mapping df
        map_al_tr = track_ids_df.copy()
        map_al_tr['Album_Id'] = album_details['id']
        
        # Add in dictionary
        al_df_dict['map_al_tr'] = map_al_tr
    
    return al_df_dict

#%% Get album information
def get_track_info(track_id,
                   get_artists = False):
    
    # Connect to my spotify app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
                                               client_secret=os.environ.get('spotify_client_secret'),
                                               redirect_uri=os.environ.get('spotify_redirect_uri'),
                                               scope="user-read-recently-played"))
    
    # Get album details and catch errors
    tra_id_df = pd.DataFrame({'Track_Id' : [track_id]})
    empty_df =  pd.DataFrame(columns = ['Track_Id'])
    try:
        track_details = sp.track(track_id)
        track_details2 = sp.audio_features(track_id)
        tr_df_dict = {'removed' : empty_df,
                      'error' : empty_df}
    except HTTPError and spotipy.SpotifyException:
        print("Album does not exist. Assume removed from spotify")
        tr_df_dict = {'removed' : tra_id_df,
                      'error' : tra_id_df}
        return tr_df_dict
    except:
        print("Other issue. ")
        tr_df_dict = {'removed' : empty_df,
                      'error' : tra_id_df}
        return tr_df_dict
    
    # Store in df
    track_details_df = pd.DataFrame({'Track_Id' : [track_details['id']],
                                      'Track_Name' : [track_details['name']],
                                      'Danceability' : [track_details2[0]['danceability']],
                                      'Energy' : [track_details2[0]['energy']],
                                      'Loudness' : [track_details2[0]['loudness']],
                                      'Speechiness' : [track_details2[0]['speechiness']],
                                      'Acousticness' : [track_details2[0]['acousticness']],
                                      'Instrumentalness' : [track_details2[0]['instrumentalness']],
                                      'Liveness' : [track_details2[0]['liveness']],
                                      'Valence' : [track_details2[0]['valence']],
                                      'Tempo' : [track_details2[0]['tempo']],
                                      'Time_Signature' : [track_details2[0]['time_signature']],
                                      'Track_Duration_ms' : [track_details['duration_ms']],
                                      'Explicit_Track' : [track_details['explicit']],
                                      'Track_Number' : [track_details['track_number']],
                                      'Disc_Number' : [track_details['disc_number']],
                                      'Key' : [track_details2[0]['key']],
                                      'Mode' : [track_details2[0]['mode']],
                                      'Track_Popularity' : [track_details['popularity']],
                                      'ISRC' : [track_details['external_ids']['isrc']]})
    
    # Store in dictionary
    tr_df_dict["track_details_df"] = track_details_df
    
    # Get albums
    album_ids_df = pd.DataFrame({'Album_Id' : [track_details['album']['id']]})
    tr_df_dict["album_ids_df"] = album_ids_df
    
    
    # Get Artists
    artist_id_list = [artist['id'] for artist in track_details['artists']]
    artist_ids_df = pd.DataFrame({'Artist_Id' : list(set(artist_id_list))})
    if get_artists:    
        tr_df_dict["artist_ids_df"] = artist_ids_df
    
    # Get track album mapping
    map_tr_al = pd.DataFrame({'Album_Id' : [track_details['album']['id']],
                              'Track_Id' : [track_id]})
    tr_df_dict["map_tr_al"] = map_tr_al
    
    # Get track artist mapping
    map_tr_ar = artist_ids_df.copy()
    map_tr_ar['Track_Id'] = track_id
    tr_df_dict["map_tr_ar"] = map_tr_ar
    
    # Get album artist mapping
    map_al_ar = artist_ids_df.copy()
    map_al_ar['Album_Id'] = track_details['album']['id']
    tr_df_dict["map_al_ar"] = map_al_ar
    
    return tr_df_dict





#%% Testing

# album_id = '1cSBYcI0dxzizxisfAk4bE'
# album_id = '00cV918s33ucbpFc5jaKI7'
# track_id = '00cqd6ZsSkLZqGMlQCR0Zo'

# # Connect to my spotify app
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('spotify_client_id'),
#                                            client_secret=os.environ.get('spotify_client_secret'),
#                                            redirect_uri=os.environ.get('spotify_redirect_uri'),
#                                            scope="user-read-recently-played"))


#test_dict = get_artist_info('0LyfQWJT6nXafLPZqxe9Of')
#test_artist2 = sp.artist_albums('0LyfQWJT6nXafLPZqxe9Of', limit=50, country="GB")
test_dict2 = get_album_info("001hiwQqutaP5krx5mhqh6")
# test_dict3 = get_track_info('00cqd6ZsSkLZqGMlQCR0Zo')

# test_rp = get_recently_played_df()
# test_rp['rec_tracks'].describe(include='all')

# track_details = sp.track(track_id) #Multiple tracks at once
# track_details2 = sp.audio_analysis(track_id) #Not this one
# track_details3 = sp.audio_features(track_id) #Multiple?


