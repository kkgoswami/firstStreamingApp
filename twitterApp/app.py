import config 
import tweepy 
from tweepy import OAuthHandler 


def parse_search_results(query):
    "return the list of user IDs that match the query."
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)


    user_id = [status.user.screen_name for status in tweepy.Cursor(api.search,q=query).items()]

    users = [api.get_user(i) for i in user_id]

    print user_id



if __name__ == '__main__':
    query = "diagnosed clinical depression"
    parse_search_results(query)


