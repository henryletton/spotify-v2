'''
    File name: hourly_spotify.py
    Author: Henry Letton
    Date created: 2021-01-26
    Python Version: 3.8.3
    Desciption: Spotify processes to run hourly 
'''

# Import modules
from src.spotify_other_fns import store_recently_played, update_artists, update_albums, update_tracks
from src.spotify_db_fns import create_engine2
from src.log_fns import log_process
# Establish database connection
engine = create_engine2()

# Every process is wrapped in logs and an error catch

# =============================================================================
# Get and store any new listens
# =============================================================================
log_process(engine, "Spotify", "Recently Played", "Start")
try:
    store_recently_played(engine)
    log_process(engine, "Spotify", "Recently Played", "End")
except:
    log_process(engine, "Spotify", "Recently Played", "Error")

# =============================================================================
# Update artist information
# =============================================================================
log_process(engine, "Spotify", "Update Artists", "Start")
try:
    update_artists(engine)
    log_process(engine, "Spotify", "Update Artists", "End")
except:
    log_process(engine, "Spotify", "Update Artists", "Error")

# =============================================================================
# Update album information
# =============================================================================
log_process(engine, "Spotify", "Update Albums", "Start")
try:
    update_albums(engine)
    log_process(engine, "Spotify", "Update Albums", "End")
except:
    log_process(engine, "Spotify", "Update Albums", "Error")

# =============================================================================
# Update track information
# =============================================================================
log_process(engine, "Spotify", "Update Tracks", "Start")
try:
    update_tracks(engine)
    log_process(engine, "Spotify", "Update Tracks", "End")
except:
    log_process(engine, "Spotify", "Update Tracks", "Error")

# =============================================================================
# Note: Warnings appear about lost mysql connection.
#       We always reconnect before using the connection and code runs fine.
# =============================================================================

