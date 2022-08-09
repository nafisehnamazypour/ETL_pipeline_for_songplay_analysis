- The purpose of this database
    A startup called Sparkify has developed a new music streaming app. So, they want to analyze the data they've been collecting 
    on songs and user activity in it. 
    The analytics team is interested in the songs which users are listening to. The whole data is stored in JSON logs and there exist
    another directory with JSON metadata on the songs.
    They need an easy way to query their data and analyze it.

- How to run the Python scripts?
    As the code is developed in .py files, it could be run by use of Terminal.
    In terminal, first,
    >>> cd directory
    and then run the script via python command:
    >>> python etl.py



- An explanation of the files in the repository : 

    sql_queries.py:
    This file contains statements to:
        first, drop tables if they already exist.
        second, creat tables(relations).
        third, insert commands to insert data into tables.

    create_tables.py : 
    This file drop tables(if they exist) and then create them by calling sql_queries.py.
    It should be executed before running etl.ipynb or etl.py to reset the tables.

    etl.ipynb:
    Within this file, the ETL process is done for each table. But, before completing the etl.py file to load the whole datasets.
    The ETL process is done for each table one by one to test them and evaluate the validation of process. 
    It, first, connects to the database and then uses python codes to read the json files conataining music files data. Then insert the 
    required data in predefined tables in database using python and sql_queries.py.

    etl.py: 
    In this file, the whole dataset is loaded by implementing the code developed in etl.ipynb. as in etl.ipynb, the data is inserted into tables 
    and data pipeline is implemented.

    test.ipynb: 
    This file has two main parts. In the first part, it connects to sparkifydb. 
    Then, it can read from different relations in database which can help us to see whether the data is added successfully to the relation or not.
    The read from relations is done via SELECT. I used this part at the end of each session to check the validation of my program.
    In the second part, some Sanity tests can be done. It helps to esnure that the project does not contain any commonly found issues.
    It checks the data type in each column of relations and return some warnings or errors in case of any issues. I used this part at the end of 
    the project to check my whole work.

    Note : All the tables are postgres tables.
    
    
- Database schema design:
    The whole database should have a star schema optimized for queries on song play analysis.     
    It has a Fact table named "songplays" and four dimension tables as follows:
    users, songs, artists and time. The parameters of these relations are as follows:
    songplays parameter :   (songplay_id serial NOT NULL PRIMARY KEY,\
                             timestamp varchar NOT NULL,\
                             user_id int NOT NULL,\
                             level varchar NOT NULL,\
                             song_id varchar,\
                             artist_id varchar,\
                             session_id int,\
                             location varchar,\
                             user_agent varchar)
                             
    users  table parameters: user_id int PRIMARY KEY,\
                             first_name varchar NOT NULL,\
                             last_name varchar NOT NULL,\
                             gender varchar,\
                             level varchar
                             
    songs table parameters:  song_id varchar PRIMARY KEY,\
                             title varchar NOT NULL,\
                             artist_id varchar NOT NULL,\
                             year int,\
                             duration float NOT NULL
                             
    artists table parameters:artist_id varchar NOT NULL PRIMARY KEY,\
                             artist_name varchar NOT NULL,\
                             location varchar,\
                             latitude float,\
                             longitude float
    
    time table parameters:   timestamp varchar,\
                             hour int,\
                             day int,\
                             week int,\
                             month int,\
                             year int,\
                             weekday int
    
 [songplays filled table example:](./screenshots/songplay_test.png)
 [users filled table example:](./screenshots/users_test.png)
 [songs filled table example:](./screenshots/songs_test.png)
 [atists filled table example:](./screenshots/artists_test.png)
 [time filled table example:](./screenshots/time_test.png)
 
 In insert queries, an 'ON CONFLICT   DO NOTHING' is used to ignore dupliaction errors like this:
 [duplication error example:](./screenshots/Duplication_error.png)
 Just in users table, the action 'DO UPDATE SET level = EXCLUDED.level' is used. Because the user level could be changed if it turns to 'paid'.


- Example queries:
    If analytics team is interested in comparison between male and female users who paid for the songs:

SELECT COUNT(DISTINCT user_id) FROM songplays WHERE gendeer="M" AND level="paid";
SELECT COUNT(DISTINCT user_id) FROM songplays WHERE gendeer="F" AND level="paid";