'''
To make it possible for multiple write fights at a time,
the id cannot be retrieved so a (server, channel) tuple is used as index
'''

def countdown(server, channel, wait, duration):
    location = (server, channel)
    try:
        if DATA[location]:
            return False
    except:
        DATA[location] = {} # creates new room group
        DATA[location]['begin_in'] = wait
        DATA[location]['duration'] = duration
        return True

def cancel(server, channel):
    location = (server, channel)
    try:
        DATA.pop(location)
        return True
    except:
        return False

DATA = {}
