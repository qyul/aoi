import discord
from discord.ext import commands

import secret #auth token, .gitignore'd
import random
import room
import wordlist

description = 'Aoi, Blue Angel Writing Bot'
bot_prefix = '::'

_data = {
    'active' : False,
    'duration' : 15
    }

aoi = commands.Bot(description=description, command_prefix=bot_prefix)

@aoi.event
async def on_ready():
    print('Login successful')
    print('Name : {}'.format(aoi.user.name))
    print('ID : {}'.format(aoi.user.id))
    print(discord.__version__)
    #print(dir(discord.Server.id))


@aoi.event
async def on_message(message):
    # prevent reply to self
    if message.author == aoi.user:
        return

    # Respond to own mentions
    if aoi.user.mentioned_in(message):
        await aoi.send_message(message.channel, '''Hiiiiii, everyone! I am Aoi, Blue Angel Writing Bot, based off Aoi Zaizen of Yugioh VRAINS (CV: Nakashima Yuki), or, `qyuli/s#7377`'s fa-vour~ite girl.''')

    # Continue to process normal bot commands
    await aoi.process_commands(message)

# Fun
@aoi.command(pass_context=True, description='Type a number after the command( ͡° ͜ʖ ͡°)')
async def lenny(ctx, n : int = 1):
    if n < 12:
        msg = ''
        rand = random.randint(0,2)

        if rand == 0:
            for i in range(n):
                msg += '    '*i + '( ͡° ͜ʖ ͡°)\n'
        elif rand == 1:
            for i in range(n):
                if i <= n/2:
                    msg += '    '*i + '( ͡° ͜ʖ ͡°)\n'
                else:
                    msg += (n-i)*'    ' + '( ͡° ͜ʖ ͡°)\n'
        else:
            for i in range(n):
                if i % 3 == 0:
                    msg += '( ͡° ͜ʖ ͡°)\n'
                else:
                    msg += '          '*random.randint(1,4) + '( ͡° ͜ʖ ͡°)\n'

        await aoi.say(msg)

    else:
        try:
            await aoi.say('( ͡° ͜ʖ ͡°)  ' * n)
        except:
            await aoi.say('Woah! Breaking that character limit( ͡° ͜ʖ ͡°)')


# Write-Fight
@aoi.group(pass_context=True)
async def fight(ctx):
    if ctx.invoked_subcommand is None:
        await aoi.say('Did you want to start a fight? Say `::fight start`, O-K?')

# start a battle
@fight.command(pass_context=True)
async def start(ctx, wait : int=5):
    room.countdown(ctx.message.server, ctx.message.channel, wait)
    await aoi.say('''O-K, let's get this write-fight started!\n\n**Beginning in {} minutes.** Type `::fight join` to enter.'''.format(wait))
    print(room.DATA)

# set the default battle duration
@fight.command()
async def time(ctx, *time):
    try:
        duration = time[0]
        _data[ctx.message.channel]['duration'] = duration

        await aoi.say(':clock: The default fight time has been set to {} minutes.'.format(duration))
    except:
        await aoi.say('The default fight time is currently {} minutes. Say `::fight time #` to change it for new fights!'.format(_data[ctx.message.channel]['duration']))

# cancel current fights
@fight.command()
async def cancel():
    if _data['active']:
        _data['active'] = False
        await aoi.say('Aw, changed your mind? Fiiiiiine ~')

    else:
        await aoi.say('There\'s no fight on now, silly.')



aoi.run(secret.token)
