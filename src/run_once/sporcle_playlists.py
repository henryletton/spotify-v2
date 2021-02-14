'''
    File name: sporcle_playlists.py
    Author: Henry Letton
    Date created: 2021-02-14
    Python Version: 3.8.3
    Desciption: Create playlist from list from sporcle quizes
'''

import pandas as pd
from src.spotify_api_fns import searches_track_ids
from src.spotify_playlist_fns import update_playlist

#%% UK TOP 5 YEAR-END SINGLES 2001-2020
uk_top5 = pd.read_csv('src/run_once/data/UK TOP 5 YEAR-END SINGLES 2001-2020.csv', 
                      encoding='latin-1', header=None)

search_list = []
n_row, n_cols = uk_top5.shape

for row in range(int(n_row/5)):
    for col in range(n_cols):
        s_row = 5*row
        e_row = 5*row + 5
        search_list.extend(list(uk_top5[col].iloc[s_row:e_row]))

track_id_list = searches_track_ids(search_list)

update_playlist('UK TOP 5 YEAR-END SINGLES 2001-2020', track_id_list, "add_order")

#%% UK TOP 5 YEAR-END SINGLES 2001-2020
uk_top6_10 = pd.read_csv('src/run_once/data/UK 6TH-10TH BIGGEST YEAR-END SINGLES 2001-2020.csv', 
                      encoding='latin-1', header=None)

search_list = []
n_row, n_cols = uk_top6_10.shape

for row in range(int(n_row/5)):
    for col in range(n_cols):
        s_row = 5*row
        e_row = 5*row + 5
        search_list.extend(list(uk_top6_10[col].iloc[s_row:e_row]))

track_id_list = searches_track_ids(search_list)

update_playlist('UK 6TH-10TH BIGGEST YEAR-END SINGLES 2001-2020', track_id_list, "add_order")

#%% UK TOP 5 YEAR-END SINGLES 2001-2020
uk_top11_15 = pd.read_csv('src/run_once/data/UK 11TH-15TH BIGGEST YEAR-END SINGLES 2001-2020.csv', 
                      encoding='latin-1', header=None)

search_list = []
n_row, n_cols = uk_top11_15.shape

for row in range(int(n_row/5)):
    for col in range(n_cols):
        s_row = 5*row
        e_row = 5*row + 5
        search_list.extend(list(uk_top11_15[col].iloc[s_row:e_row]))

track_id_list = searches_track_ids(search_list)

update_playlist('UK 11TH-15TH BIGGEST YEAR-END SINGLES 2001-2020', track_id_list, "add_order")

