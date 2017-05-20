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
    sql = ''' INSERT INTO search_results(user_screen_name, status, tweet_id, isDepressed) VALUES(?,?,?,?)'''
    cur = conn.cursor()
    try: 
        cur.execute(sql, search)
        conn.commit()
    except sqlite3.IntegrityError as e:
        pass 

    n = cur.lastrowid
    conn.close()
    return n

def get_user_data(user_screen_name, label):
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    user = api.get_user(user_screen_name)
    user_data = (user.screen_name, user.location, user.created_at, user.statuses_count, user.friends_count, user.name, label)
    return add_user(create_connection('twitter.sqlite'), user_data)

def gather_user_timeline():
    sql = '''select user_screen_name, isDepressed from search_results'''
    conn = create_connection('twitter.sqlite')
    cur = conn.cursor()
    cur.execute(sql)
    users = cur.fetchall()
    conn.close()
    for user in users:
        if user[1] == 0:
            get_user_data(str(user[0]), (user[1]))
        elif user[1] == "True":  
            get_user_data(str(user[0]), 1) 

        get_all_tweets(user[0])

def get_all_tweets(user_screen_name):
    """returns the recent 3240 tweets of the user."""
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    alltweets = []
    new_tweets = api.user_timeline(screen_name=user_screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=user_screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    for tweet in alltweets:
        data = (tweet.id_str,tweet.user.screen_name,tweet.text,tweet.created_at)
        add_tweet(create_connection('twitter.sqlite'), data)  

    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]


def add_user(conn, user): 
    sql = '''INSERT INTO users(user_screen_name, location, created_at, num_status, num_friends, num_followers, name, isDepressed) VALUES (?,?,?,?,?,?,?,?)'''
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
                search = (status.user.screen_name, status.text, status.id, False)
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
    gather_user_timeline()
    #query = "hey"
    

