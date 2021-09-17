'''
    File name: daily_spotify.py
    Author: Henry Letton
    Date created: 2021-02-06
    Python Version: 3.8.3
    Desciption: Spotify processes to run daily 
'''

# Import modules
from src.spotify_playlist_fns import playlist_total_plays, sql_update_playlist
from src.spotify_db_fns import create_engine2
from src.log_fns import log_process
# Establish database connection
engine = create_engine2()

# Log start of playlist refresh
log_process(engine, "Spotify", "Refresh Playlists", "Start")

# =============================================================================
# Refresh all smart playlists related to track listens
# =============================================================================

playlist_total_plays(engine, "Spotify Library", 1)
playlist_total_plays(engine, "2+ Listens", 2)
playlist_total_plays(engine, "5+ Listens", 5)


# =============================================================================
# Playlist of songs I listened 5+ times in iTunes, but neve on Spotify
# =============================================================================
sql_update_playlist(engine, "Only iTunes Listens", """
SELECT a.Track_Id
FROM
    (SELECT 
        Track_Id,
        SUM(Plays) as iTunes_Plays
    FROM Music_Track_Listens
    WHERE Source = 'iTunes'
    GROUP BY Track_Id)
AS a
LEFT JOIN
    (SELECT 
        Track_Id,
        SUM(Plays) as Spotify_Plays
    FROM Music_Track_Listens
    WHERE Source != 'iTunes'
    GROUP BY Track_Id)
AS b
ON a.Track_Id = b.Track_Id
WHERE Spotify_Plays IS NULL
AND iTunes_Plays >= 5;
""")

# =============================================================================
# Playlist of songs played on this day in previous years (OneDrive "photos On This Day")
# =============================================================================
sql_update_playlist(engine, "On This Day", """
SELECT Track_Id 
    FROM `Music_Track_Listens`
        WHERE MONTH(DateTime) = MONTH(curdate())
        AND DAY(DateTime) = DAY(curdate())
        AND DATE(DateTime) != curdate();
""")


# Log end of playlist refresh
log_process(engine, "Spotify", "Refresh Playlists", "End")