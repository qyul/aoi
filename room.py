'''
To make it possible for multiple write fights at a time,
a (server, channel) tuple is used as index (id cannot be retrieved)
'''

active_rooms = {}
past_rooms = {}

def identify(ctx):
    return (ctx.message.server, ctx.message.channel)

def start(ctx, nonce):
    location = identify(ctx)
    if location in active_rooms:
        return False
    else:
        # create room
        active_rooms[location] = {'nonce': nonce}
        return True

def active(ctx, *nonce):
    location = identify(ctx)
    if location in active_rooms:
        if nonce:
            if nonce[0] != active_rooms[location]['nonce']:
                #print('nonce error.')
                return False
        return True
    else:
        return False

def terminate(ctx, completed=False):
    location = identify(ctx)
    if location in active_rooms:
        if completed:
            #move participant list to historical data
            past_rooms[location] = active_rooms[location]
        active_rooms.pop(location)
        return True
    else:
        return False

def add_participant(ctx):
    location = identify(ctx)
    try:
        active_rooms[location][ctx.message.author] = 'Unknown'
        return True
    except:
        return False

def update_participant(ctx, comment):
    location = identify(ctx)
    try:
        past_rooms[location][ctx.message.author] = comment
        return True
    except:
        return False

def get_participants(ctx):
    location = identify(ctx)
    try:
        mentionable = []
        for entry in active_rooms[location]:
            try:
                mentionable.append(entry.mention)
            except:
                pass
        return mentionable
    except:
        print('error')

def generate_results(ctx):
    location = identify(ctx)
    try:
        past_rooms[location].pop('nonce')
        results = past_rooms[location]
    except:
        results = False
        
    past_rooms.pop(location) # delete participant listing
    
    return results


##def testresult(ctx, name, res):
##    location = identify(ctx)
##    past_rooms[location][name] = res
##
##def testplayer(ctx, name):
##    location = identify(ctx)
##    active_rooms[location][name] = 'Unknown'
