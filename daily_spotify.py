'''
    File name: daily_spotify.py
    Author: Henry Letton
    Date created: 2021-02-06
    Python Version: 3.8.3
    Desciption: Spotify processes to run daily 
'''

# Import modules
from src.spotify_playlist_fns import playlist_total_plays
from src.spotify_db_fns import create_engine2
from src.log_fns import log_process
# Establish database connection
engine = create_engine2()

# =============================================================================
# Refresh all smart playlists related to track listens
# =============================================================================
log_process(engine, "Spotify", "Refresh Playlists", "Start")
playlist_total_plays(engine, "Spotify Library", 1)
playlist_total_plays(engine, "2+ Listens", 2)
playlist_total_plays(engine, "5+ Listens", 5)
log_process(engine, "Spotify", "Refresh Playlists", "end")

