'''
    File name: hourly_spotify.py
    Author: Henry Letton
    Date created: 2021-01-26
    Python Version: 3.8.3
    Desciption: Spotify processes to run hourly 
'''

from src.spotify_other_fns import store_recently_played, update_artists, update_albums, update_tracks
from src.spotify_db_fns import create_engine2
from datetime import datetime

engine = create_engine2()

store_recently_played(engine)

print(datetime.now())
update_artists(engine)
print(datetime.now())

update_albums(engine)
print(datetime.now())

update_tracks(engine)
print(datetime.now())

