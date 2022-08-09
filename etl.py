import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime, time
import numpy as np


def process_song_file(cur, filepath):
    """In this function songs table and artists table are filled with
    values from json files in filepath using insert queris from sql_queries.py
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values
    song_data = song_data[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude','artist_longitude']].values 
    artist_data = artist_data[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """In this function the data is filtered by 'NextSong' in page column and then 
    the hour, day, week of year, month, year and weekday are extracted from timestamp 
    and inserted into time table using insert queris from sql_queries.py
    The users table is also filled with 'userId', 'firstName', 'lastName', 'gender', 'level'.
    Nest, songsplay table is filled with selected data from songs table. As the aong_id and artist_id
    should be selected from songs and artists table, the select query is used to join these tables and
    select the relevant data from them in an itterative process for each column in df datafram(which is
    filtered by 'NestSong')
    """
    # open log file
    #log_files = read_json(filepath, lines=True)
    #filepath = log_files[0]
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=="NextSong"]

    # convert timestamp column to datetime
    t = [None]*len(df)
    i = 0
    for item in df['ts']:
        t[i] = datetime.datetime.fromtimestamp(int(item/1000)) 
        i = i+1
    t = pd.Series(t)
    
    # insert time data records 
    column_labels = ('time_stamp','hour', 'day', 'week_of_year', 'month', 'year', 'weekday')
    time_data = [None]*7
    time_data[0] = [t]
    time_data[1] = [t.dt.hour]
    time_data[2] = [ t.dt.day]
    time_data[3] = [ t.dt.weekofyear]
    time_data[4] = [t.dt.month]
    time_data[5] = [t.dt.year]
    time_data[6] = [t.dt.weekday]
    time_df = pd.DataFrame(data = list(zip(t, t.dt.hour,t.dt.day,t.dt.weekofyear,t.dt.month,t.dt.year,t.dt.weekday)), columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
            #print(results)
            #print(index)
        else:
            songid, artistid = None, None
            # insert songplay record
        t_temp = datetime.datetime.fromtimestamp(int(row.ts/1000))
        songplay_data = (t_temp , int(row.userId), str(row.level), str(songid), str(artistid), int(row.sessionId), str(row.location), str(row.userAgent))
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """In this function the whole data is read from all files in the filepath
    one by one and prints how many files are found and which file is processed
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """This is the main function of the program in which the connection and curser are made and
    the process_song_file and process_log_file are called to process the files in the filepath one by one
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()