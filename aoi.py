import discord
from discord.ext import commands

import secret    # auth token, .gitignore'd
import random    # random generator
import room      # multiple server-channel instances
import starters  # prompt lists

description = 'Aoi, Blue Angel Writing Bot (by qyuli/s#7377)'
bot_prefix = '::'

_data = {
    'active' : False,
    'duration' : 15
    }

def rand_emoji(*args):
    return random.choice(args)

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
        await aoi.send_message(message.channel, '''Hiiiiii, everyone! I am Aoi, Blue Angel Writing Bot, based off Aoi Zaizen of *Yugioh VRAINS* (CV: Nakashima Yuki). A.k.a., `qyuli/s#7377`'s current best girl.''')

    # Continue to process normal bot commands
    await aoi.process_commands(message)

# Fun
@aoi.command(pass_context=True, description='Type a number( ͡° ͜ʖ ͡°)')
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


#::random word
@aoi.group(pass_context=True, description='Picks from a list. Sub-commands required.')
async def starter(ctx):
    if ctx.invoked_subcommand is None:
        await aoi.say('Be clearer! `::help starter` to see options !')

@starter.command(pass_context=True)
async def word(ctx):
    w = starters.rand_word()
    await aoi.say(':star: - `{}` - :star:'.format(w))

@starter.command(pass_context=True)
async def prompt(ctx):
    entry = starters.rand_prompt()
    emoji = rand_emoji('point_right')
    await aoi.say('<http://twitter.com/{}/status/{}>\n:{}: `{}`'
                  .format(entry['user'], entry['id'], emoji, entry['text']))

@starter.command(pass_context=True)
async def sff(ctx):
    entry = starters.rand_sff()
    emoji = rand_emoji('rocket','milky_way','space_invader','comet','dizzy','new_moon_with_face', 'pager')
    await aoi.say('<http://twitter.com/{}/status/{}>\n:{}: `{}`'
                  .format(entry['user'], entry['id'], emoji, entry['text']))
    
@starter.command(pass_context=True)
async def omen(ctx):
    entry = starters.rand_omen()
    emoji = rand_emoji('grey_question', 'zap', 'cyclone', 'four_leaf_clover', 'paw_prints', 'seedling', 'ghost', 'skull', 'see_no_evil')
    await aoi.say('<http://twitter.com/{}/status/{}>\n:{}: `{}`'
                  .format(entry['user'], entry['id'], emoji, entry['text']))

    
# Write-Fight
@aoi.group(pass_context=True, description='Begin a word war.\n\'::fight start @ #\', where @ and # are optional numbers.\n@ = countdown, # = duration')
async def fight(ctx):
    if ctx.invoked_subcommand is None:
        await aoi.say('Did you want to start a fight? Say `::fight start`, O-K?')

# start a battle
@fight.command(pass_context=True)
async def start(ctx, wait:int=5, duration:int=15):
    success = room.countdown(ctx.message.server, ctx.message.channel, wait, duration)

    if success:
        await aoi.say('''O-K, let's get this write-fight started!\n\n**Beginning in {} minutes for {} minutes.** Type `::fight join` to enter.'''.format(wait, duration))
    else:
        await aoi.say('''Hey, one battle at a time, O-K?''')        

# cancel current battle
@fight.command(pass_context=True)
async def cancel(ctx):
    if room.cancel(ctx.message.server, ctx.message.channel):
        await aoi.say('Aw, changed your mind? Fiiiiiine ~')
    else:
        await aoi.say('There\'s no fight on here, silly.')


aoi.run(secret.token)
