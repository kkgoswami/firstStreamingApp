import config
import csv
import tweepy 
from tweepy import OAuthHandler


def parse_search_results(query):
    "return the list of user IDs that match the query."
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)


    user_id = [status.user.screen_name for status in tweepy.Cursor(api.search,q=query).items()]

    users = [get_all_tweets(api, i) for i in user_id]


def get_all_tweets(api, user_screen_name):
    """returns the recent 3240 tweets of the user."""

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

    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    with open('%s_tweets.csv' % user_screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass



if __name__ == '__main__':
    query = "diagnosed clinical depression"
    parse_search_results(query)


