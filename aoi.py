import discord
from discord.ext import commands

import secret

description = 'Aoi, Blue Angel Writing Bot'
bot_prefix = '::'

_fight = {
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

@aoi.command(pass_context=True)
async def test(ctx):
    await aoi.say('Understood.')

@aoi.command(pass_context=True)
async def test2(ctx):
    await aoi.say('ok')

@aoi.group(pass_context=True)
async def fight(ctx):
    if ctx.invoked_subcommand is None:
        await aoi.say('Did you want to start a fight? Say `::fight start`, O-K?')

@fight.command()
async def start(*time):
    try:
        countdown = time[0]
    except:
        countdown = 5

    _fight['active'] = True
    await aoi.say('''O-K, let's get this write-fight started!\n\n**Beginning in {} minutes.** Type `::fight join` to enter.'''.format(countdown))

@fight.command(pass_context=True)
async def time(ctx, *time):
    #print(ctx.message.channel_id)
    try:
        duration = time[0]
        _fight['duration'] = duration

        await aoi.say(':clock: The default fight time has been set to {} minutes.'.format(_fight['duration']))
    except:
        await aoi.say('The default fight time is currently {} minutes. Say `::fight time #` to change it for new fights!'.format(_fight['duration']))


@fight.command()
async def cancel():
    if _fight['active']:
        _fight['active'] = False
        await aoi.say('Aw, changed your mind? Fiiiiiine ~')

    else:
        await aoi.say('There\'s no fight on now, silly.')


aoi.run(secret.token)
