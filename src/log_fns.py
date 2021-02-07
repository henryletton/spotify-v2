'''
    File name: log_fns.py
    Author: Henry Letton
    Date created: 2021-02-07
    Python Version: 3.8.3
    Desciption: Functions that interact with the MySQL database
'''

#%% Function to log a step in a regular process
def log_process(engine,
                project = "",
                process = "",
                details = ""):
    
    # Connect to database
    engine.connect()
    
    query = """INSERT INTO Event_Log
                (Project, Process, Details)
                VALUES (%s, %s, %s);
                """
    
    insert_values = (project, process, details)
    
    with engine.begin() as cnx:
        cnx.execute(query, insert_values)

    return query


