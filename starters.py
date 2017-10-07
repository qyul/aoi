import random
import twitter
import secret
import re

with open('wordlist.txt') as f:
    WORDLIST = f.read().splitlines()

def rand_word():
    return random.choice(WORDLIST)

api = twitter.Api(consumer_key=secret.twitter[0],
                  consumer_secret=secret.twitter[1],
                  access_token_key=secret.twitter[2],
                  access_token_secret=secret.twitter[3])
twitter_ids = {
    'howboutyouwrite': 3300806993,
    'sff_prompt_bot': 854481108871725056,
    'omensbot' : 4196463141,
    'autodoyle' : 3229361280,
    'dreamhaver' : 3360143685,
    'cityexplorerbot' : 4861670522
}
def rand_tweet(name):
    tweets = api.GetUserTimeline(twitter_ids[name])
    tweet = random.choice(tweets)
    
    entry = {'user' : tweet.user.screen_name,
             'id' : tweet.id}

    #strip hashtags
    r = re.compile('\s#\S+')
    entry['text'] = r.sub('', tweet.text)
    
    return entry

def rand_prompt():
    return rand_tweet('howboutyouwrite')

def rand_sff():
    return rand_tweet('sff_prompt_bot')

def rand_omen():
    return rand_tweet('omensbot')

def rand_dream():
    return rand_tweet('dreamhaver')

def rand_explore():
    return rand_tweet('cityexplorerbot')

