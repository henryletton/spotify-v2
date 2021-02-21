'''
    File name: spotify_db_fns.py
    Author: Henry Letton
    Date created: 2021-01-20
    Python Version: 3.8.3
    Desciption: Functions that interact with the MySQL database
'''

#%% Import any modules required for the functions
from sqlalchemy import create_engine 
from random import randrange
import pandas as pd
import os

#%% Load system variables from .env file
from dotenv import load_dotenv
load_dotenv()

#%% Function to establish connection to db
def create_engine2(sql_user = os.environ.get("sql_user"),
                   sql_pw = os.environ.get("sql_pw"),
                   sql_db = os.environ.get("sql_db")):
    
    # Link to database
    db_url = f'mysql+mysqlconnector://{sql_user}:{sql_pw}@{sql_db}'
    engine = create_engine(db_url)
    
    return engine


#%% Function to write a dataframe to sql database
def df_to_sql_db(engine,
              df_write,
              table_name,
              mid_table_name = 'temporary_table',
              replace = False):
    
    # Connect to database
    engine.connect()
    
    # Replacing rows requires different sql syntax to ignoring
    if replace:
        replace_or_ignore = 'REPLACE'
    else:
        replace_or_ignore = 'INSERT IGNORE'
    
    # Dedupe df 
    df_write = df_write.drop_duplicates()
    
    # With connection, insert rows
    with engine.begin() as cnx:
        
        # Middle temporary table used to utilise both to_sql method and "insert 
        # ignore" sql syntax
        temp_table_name = f'{mid_table_name}_{randrange(100000)}' #randomrange keeps overlap risk minimal
        
        # Remove table if left over from a failed previous process
        drop_table_sql = f'DROP TABLE IF EXISTS {temp_table_name}'
        cnx.execute(drop_table_sql)
        
        # Middle temporary table has the same schema to final table
        create_table_sql = f'CREATE TABLE {temp_table_name} LIKE {table_name}'
        cnx.execute(create_table_sql)
        
        # Write data to temp table
        df_write.to_sql(con=engine, name=temp_table_name, if_exists='append', index = False)
        
        # Move data to actual table, replacing/ignoring according to primary keys
        insert_sql = f'{replace_or_ignore} INTO {table_name} (SELECT * FROM {temp_table_name})'
        cnx.execute(insert_sql)
        
        # Remove middle temporary table
        drop_table_sql = f'DROP TABLE IF EXISTS {temp_table_name}'
        cnx.execute(drop_table_sql)
    
    return

#%% Function to read complete table from database
def sql_db_to_df(engine,
                 table_name):
    
    # Connect to database
    engine.connect()
    
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', engine)
    
    return df
    
#%% Function to flag artist/album/track as removed from spotify
def removed_from_spotify(engine, given_ids, id_type):
    
    # Connect to database
    engine.connect()
    
    for given_id in given_ids[f'{id_type}_Id']:
        # Query to update table
        sql_query = f'UPDATE Music_{id_type}s Removed_{id_type} = 1 WHERE {id_type}_Id = "{given_id}"'
        
        # Run query
        with engine.begin() as cnx:
            cnx.execute(sql_query)
    
    return
    
#%% Get dataframe from given sql
def df_from_sql(engine,
                sql_query):
    
    # Connect to database
    engine.connect()
    
    # Execute query and return dataframe
    try:
        df = pd.read_sql_query(sql_query, engine)
        return df
    
    except:
        print('Query failed. Empty dataframe returned.')
        return pd.DataFrame()
    




