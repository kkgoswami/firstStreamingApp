import sqlite3

twitterdb = 'twitter.sqlite'
table_1 = 'users'
table_2 = 'search_results'
table_3 = 'tweets'

conn = sqlite3.connect(twitterdb)
c = conn.cursor()

search_table = """ CREATE TABLE IF NOT EXISTS search_results (
                       user_screen_name text PRIMARY KEY, 
                       status text, 
                       tweet_id text
                       ); """

user_table = """ CREATE TABLE IF NOT EXISTS users ( 
                     user_screen_name text PRIMARY KEY,
                     location text, 
                     created_at text, 
                     num_status integer, 
                     num_friends integer, 
                     num_followers integer
                     name text
                     );"""

tweet_table = """ CREATE TABLE IF NOT EXISTS tweets (
                      tweet_id text PRIMARY KEY, 
                      user_screen_name text, 
                      tweet_text text, 
                      time text
                      );"""

try: 
    c.execute(search_table)
    c.execute(user_table)
    c.execute(tweet_table)
except Error as e: 
    print(e)

