import config
import tweepy 
from tweepy import OAuthHandler
import sqlite3
import time

# clinical depression
# diagnosed clinical depression
# have clinical depression
# developed clinical depression
# developed depression
# suffering from depression

def create_connection(database):
    try: 
        conn = sqlite3.connect(database)
        return conn
    except Exception as e: 
        print(e)
        
    return None

def add_search_result(conn, search): 
    sql = ''' INSERT INTO search_results(user_screen_name, status, tweet_id) VALUES(?,?,?)'''
    cur = conn.cursor()
    try: 
        cur.execute(sql, search)
        conn.commit()
    except sqlite3.IntegrityError as e:
        pass 

    n = cur.lastrowid
    conn.close()
    return n

def add_user(conn, user): 
    sql = '''INSERT INTO users(user_screen_name, location, created_at, num_status, num_friends, num_followers, name) VALUES (?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    try: 
        cur.execute(sql, user)
        conn.commit()
    except sqlite3.IntegrityError as e:
        pass
    
    n = cur.lastrowid
    conn.close()
    return n


def add_tweet(conn, tweet): 
    sql -'''INSERT INTO tweets(tweet_id, user_screen_name, tweet_text, time) VALUES(?,?,?,?)'''
    cur = conn.cursor()
    try: 
        cur.execute(sql, tweet)
        conn.commit()
    except sqlite3.IntegrityError as e:
        pass

    n = cur.lastrowid
    conn.close()
    return n

def search_results(query):
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
   
    c = tweepy.Cursor(api.search,q=query).items()

    while True: 
        try: 
            status = c.next()
            if (not status.retweeted) and ('RT @' not in status.text):
                search = (status.user.screen_name, status.text, status.id)
                print add_search_result(create_connection('twitter.sqlite'), search)
        except tweepy.TweepError:
            print "sleeping for 15 minutes"
            time.sleep(60*15)
            continue
        except StopIteration: 
            break


def get_user_timeline(username):
    pass


if __name__ == '__main__': 
    query = "suffering from depression"
    search_results(query)

