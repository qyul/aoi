'''
To make it possible for multiple write fights at a time,
the id cannot be retrieved so a (server, channel) tuple is used as index
'''

##class Room(object):
##    server = ''
##    channel = ''
##
##    def __init__(self, server, channel):
##        self.server = server
##        self.channel = channel
##
##def register(server, channel):
##    room = Room(server, channel)
##    return room

def countdown(server, channel, wait):
    location = (server, channel)
    try:
        if DATA[location]:
            return False
    except:
        DATA[location] = {} # creates new room group
        DATA[location]['active'] = True
        DATA[location]['begin_in'] = wait
        return True

DATA = {}
