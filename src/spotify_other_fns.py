'''
    File name: spotify_other_fns.py
    Author: Henry Letton
    Date created: 2021-01-20
    Python Version: 3.8.3
    Desciption: Functions that either interact with both the Spotify API and 
                my MySQL database, or neither
'''

#%% Import any modules required for the functions
from src.spotify_api_fns import get_recently_played_df, get_artist_info, get_album_info, get_track_info
from src.spotify_db_fns import df_to_sql_db, sql_db_to_df, removed_from_spotify
from src.spotify_playlist_fns import update_playlist

#%% Consolidate a list of get_info dictionaries
def consolidate_dict_list(dict_list):
    
    # Start with empty list
    consolidated_dict = {}
        
    for single_dict in dict_list:
        # For each dict, either add new key or append to main dict
        for key, value in single_dict.items():
            
            if key in consolidated_dict:
                consolidated_dict[key] = consolidated_dict[key].append(value, ignore_index = True)
                
            else:
                consolidated_dict[key] = value
                
    return consolidated_dict

#%% Combine spotify and db functions to store recently played from api
def store_recently_played(engine, get_dfs = False):
    
    # Get recently played as dictionary of dataframes
    dataframe_dict = get_recently_played_df()
    
    #Store each dataframe in turn
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['rec_tracks'],
                 table_name = "Music_Track_Listens")
    
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['rec_tracks'][['Track_Id']],
                 table_name = "Music_Tracks")
    
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['rec_albums'],
                 table_name = "Music_Albums")
    
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['rec_artists'],
                 table_name = "Music_Artists")
    
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['map_tr_al'],
                 table_name = "Music_Album_Track_Mapping")
    
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['map_tr_ar'],
                 table_name = "Music_Artist_Track_Mapping")
    
    df_to_sql_db(engine = engine,
                 df_write = dataframe_dict['map_al_ar'],
                 table_name = "Music_Artist_Album_Mapping")
    
    # Update Recently Played playlist
    update_playlist("50 Recently Played Songs", dataframe_dict['rec_tracks']['Track_Id'].tolist())

    # Dataframe dict can be output if specified
    if get_dfs:
        return dataframe_dict
    else:
        return

#%% Update artist information
def update_artists(engine, update_albums = True):
    
    # Connect to database
    engine.connect()
    
    # Get priority artist ids
    Music_Refresh_Artist = sql_db_to_df(engine = engine, 
                                        table_name = 'Music_Refresh_Artist')
    # Get list of dicts
    list_of_dicts = [get_artist_info(artist_id = artist_id, get_albums = update_albums) for artist_id in Music_Refresh_Artist['Artist_Id']]
    
    # Convert list to one dict
    artists_dict = consolidate_dict_list(list_of_dicts)
        
    # Connect to database
    engine.connect()
    
    # If no error then store information
    if 'artist_details_df' in artists_dict.keys():
        
        df_to_sql_db(engine = engine,
             df_write = artists_dict['artist_details_df'],
             table_name = "Music_Artists",
             replace = True)
        
        # Not all artist have genres
        if 'artist_genres_df' in artists_dict:
            df_to_sql_db(engine = engine,
                 df_write = artists_dict['artist_genres_df'],
                 table_name = "Music_Genres")
        
        # Only have/store album information if specified
        if update_albums:
            
            df_to_sql_db(engine = engine,
                 df_write = artists_dict['album_ids_df'],
                 table_name = "Music_Albums")
            
            df_to_sql_db(engine = engine,
                 df_write = artists_dict['map_al_ar'],
                 table_name = "Music_Artist_Album_Mapping")
        
    # If artist has been removed from spotify
    if 'removed' in artists_dict.keys() and not artists_dict['removed'].empty:
        print('Mark as removed')
        removed_from_spotify(engine, artists_dict['removed'], 'Artist')
    
    return

#%% Update album information
def update_albums(engine, update_tracks = False):
    
    # Connect to database
    engine.connect()
    
    # Get priority artist ids
    Music_Refresh_Album = sql_db_to_df(engine = engine, 
                                       table_name = 'Music_Refresh_Album')
    
    # Get list of dicts
    list_of_dicts = [get_album_info(album_id, update_tracks) for album_id in Music_Refresh_Album['Album_Id']]
    
    # Convert list to one dict
    albums_dict = consolidate_dict_list(list_of_dicts)
        
    # Connect to database
    engine.connect()
    
    # If no error then store information
    if 'album_details_df' in albums_dict.keys():
        
        df_to_sql_db(engine = engine,
                     df_write = albums_dict['album_details_df'],
                     table_name = "Music_Albums",
                     replace = True)
        
        # Not all albums have genres
        if 'album_genres_df' in albums_dict:
            df_to_sql_db(engine = engine,
                 df_write = albums_dict['album_genres_df'],
                 table_name = "Music_Genres")
        
        # Only have/store track information if specified
        if update_tracks:
            
            df_to_sql_db(engine = engine,
                 df_write = albums_dict['track_ids_df'],
                 table_name = "Music_Tracks")
            
            df_to_sql_db(engine = engine,
                 df_write = albums_dict['map_al_tr'],
                 table_name = "Music_Album_Track_Mapping")
        
    # If artist has been removed from spotify
    if 'removed' in albums_dict.keys() and not albums_dict['removed'].empty:
        print('Mark as removed')
        removed_from_spotify(engine, albums_dict['removed'], 'Album')
    
    return

#%% Update track information
def update_tracks(engine, update_artists = False):
    
    # Connect to database
    engine.connect()
    
    # Get priority track ids
    Music_Refresh_Track = sql_db_to_df(engine = engine, 
                                       table_name = 'Music_Refresh_Track')
    
    # Get list of dicts
    list_of_dicts = [get_track_info(track_id, get_artists = update_artists) for track_id in Music_Refresh_Track['Track_Id']]
    
    # Convert list to one dict
    tracks_dict = consolidate_dict_list(list_of_dicts)
        
    # Connect to database
    engine.connect()
    
    # If no error then store information
    if 'track_details_df' in tracks_dict.keys():
            
        df_to_sql_db(engine = engine,
             df_write = tracks_dict['track_details_df'],
             table_name = "Music_Tracks",
             replace = True)
        
        df_to_sql_db(engine = engine,
             df_write = tracks_dict['album_ids_df'],
             table_name = "Music_Albums")
        
        if update_artists:
            df_to_sql_db(engine = engine,
                 df_write = tracks_dict['artist_ids_df'],
                 table_name = "Music_Artists")
        
        df_to_sql_db(engine = engine,
             df_write = tracks_dict['map_al_ar'],
             table_name = "Music_Artist_Album_Mapping")
        
        df_to_sql_db(engine = engine,
             df_write = tracks_dict['map_tr_al'],
             table_name = "Music_Album_Track_Mapping")
        
        df_to_sql_db(engine = engine,
             df_write = tracks_dict['map_tr_ar'],
             table_name = "Music_Artist_Track_Mapping")

            
     # If artist has been removed from spotify
    if 'removed' in tracks_dict.keys() and not tracks_dict['removed'].empty:
        print('Mark as removed')
        removed_from_spotify(engine, tracks_dict['removed'], 'Track')
    
    return



