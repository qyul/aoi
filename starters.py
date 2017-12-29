import os
import random
import twitter
import re
import json

def rand_word():
    with open('wordlist.txt') as f:
        wordlist = f.read().splitlines()
    
    return random.choice(wordlist)

api = twitter.Api(consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
                  consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
                  access_token_key=os.getenv('TWITTER_ACCESS_TOKEN'),
                  access_token_secret=os.getenv('TWITTER_ACCESS_SECRET'))
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

def tweet_formatter(user):
    def decorator(emoji):
        def wrapper():
            tweet = rand_tweet(user)
            #print(tweet)
            return '<http://twitter.com/{}/status/{}>\n:{}: `{}`'.format(tweet['user'], tweet['id'], emoji(), tweet['text'])
        return wrapper
    return decorator

#prompt
@tweet_formatter('howboutyouwrite')
def rand_prompt():
    emoji = random.choice(['point_right'])
    return emoji

#scifi fantasy
@tweet_formatter('sff_prompt_bot')
def rand_sff():
    emoji = random.choice(['rocket',
                           'milky_way',
                           'space_invader',
                           'comet',
                           'dizzy',
                           'new_moon_with_face',
                           'pager'])
    return emoji

#omens
@tweet_formatter('omensbot')
def rand_omen():
    emoji = random.choice(['grey_question',
                           'zap',
                           'cyclone',
                           'four_leaf_clover',
                           'paw_prints',
                           'seedling',
                           'ghost',
                           'skull',
                           'see_no_evil'])
    return emoji

#casemaker
@tweet_formatter('autodoyle')
def rand_doyle():
    emoji = random.choice(['mag',
                           'mag_right',
                           'spy',
                           'cop',
                           'dark_sunglasses',
                           'knife',
                           'grey_question',
                           'grey_exclamation',
                           'boom',
                           'oncoming_police_car'])
    return emoji

#dreams
@tweet_formatter('dreamhaver')
def rand_dream():
    emoji = random.choice(['crystal_ball',
                           'low_brightness',
                           'partly_sunny',
                           'bookmark',
                           'memo',
                           'ear_of_rice',
                           'snowflake',
                           'dash'])
    return emoji

#city explorer
@tweet_formatter('cityexplorerbot')
def rand_explore():
    emoji = random.choice(['notes',
                           'foggy',
                           'radio',
                           'watch',
                           'postbox',
                           'door',
                           'clapper',
                           'black_joker',
                           'hotel',
                           'office',
                           'car',
                           'taxi'])
    return emoji

#moodbot_
# moodbot_ is a special case in that it is no longer regularly updated,
# so the normal "pick a random tweet from the 20 recent tweets" method 
# will not work. Thus its tweets have been fetched into a local file.
def rand_mood():
    with open('moodlist.json') as json_data:
        d = json.load(json_data)

    tweet_text = random.choice(list(d["moods"]))
    tweet_id = d["moods"][tweet_text]

    emoji = random.choice(['herb',
                           'shamrock',
                           'maple_leaf',
                           'ear_of_rice',
                           'hibiscus',
                           'sunflower',
                           'tulip',
                           'blossom'])

    return '<http://twitter.com/moodbot_/status/{}>\n:{}: `{}`'.format(tweet_id, emoji, tweet_text)
