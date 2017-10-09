import discord
from discord.ext import commands

import os
import datetime
import random
import room      # multiple server-channel instances
import asyncio
import starters  # prompt lists

version_string = '0.9 bughunting'
description = 'Aoi, Blue Angel Writing Bot (by qyuli/s#7377)\nver. ' + version_string
bot_prefix = '::'

aoi = commands.Bot(description=description, command_prefix=bot_prefix)

@aoi.event
async def on_ready():
    print('Login successful')
    print('Name : {}'.format(aoi.user.name))
    print('ID : {}'.format(aoi.user.id))
    print(datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y"))
    print(discord.__version__)


@aoi.event
async def on_message(message):
    # prevent reply to self
    if message.author == aoi.user:
        return

    # Respond to own mentions
    if aoi.user.mentioned_in(message):
        await aoi.send_message(message.channel, 'Hiiiiii, everyone! I am Aoi, Blue Angel Writing Bot, based off Aoi Zaizen of *Yugioh VRAINS* (CV: Nakashima Yuki). A.k.a., `qyuli/s#7377`\'s fa-vour~ite girl.\n\nSee `::help` for commands!')

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
@aoi.group(pass_context=True, help='Picks from a list. Sub-command required.')
async def starter(ctx):
    if ctx.invoked_subcommand is None:
        await aoi.say('Be clearer! `::help starter` to see options☆')

@starter.command(pass_context=True, help='Random word')
async def word(ctx):
    w = starters.rand_word()
    await aoi.say(':star: - `{}` - :star:'.format(w))

@starter.command(pass_context=True)
async def prompt(ctx):
    await aoi.say(starters.rand_prompt())

@starter.command(pass_context=True, help='Science fiction/fantasy')
async def sff(ctx):
    await aoi.say(starters.rand_sff())
    
@starter.command(pass_context=True)
async def omen(ctx):
    await aoi.say(starters.rand_omen())

@starter.command(pass_context=True, help='Mystery titles')
async def doyle(ctx):
    await aoi.say(starters.rand_doyle())

@starter.command(pass_context=True)
async def dream(ctx):
    await aoi.say(starters.rand_dream())

@starter.command(pass_context=True, help='City explorer')
async def explore(ctx):
    await aoi.say(starters.rand_explore())

    
# Write-Fight
@aoi.group(pass_context=True, help='Begin a word war')
async def fight(ctx):
    if ctx.invoked_subcommand is None:
        await aoi.say(random.choice(['Did you want to start a fight? Say `::fight start`, O-K?',
                                     'There\'s no fight on right now. Try `::fight start` if you wanted to go!'
                                     ]))

# start a battle
@fight.command(pass_context=True, help='[wait=5] [duration=15]')
async def start(ctx, wait:int=5, duration:int=15):
    nonce = random.getrandbits(24)
    success = room.start(ctx, nonce)
    
    if success:
        await aoi.say(random.choice(['O-K, let\'s get this write-fight started!',
                                     'Let\'s do this, here we go!']) + '\n\n**Beginning in {} minutes for {} minutes.** Type `::fight join` to enter.'.format(wait, duration))
        room.add_participant(ctx)
        await asyncio.sleep(wait*60)

        # check if fight is still active after wait
        if not room.active(ctx, nonce):
            return

        players = ', '.join(room.get_participants(ctx))
        await aoi.say(random.choice([
                        'Here we go. {}, fiiiiiiight start!'.format(players),
                        '{}. Ready? GO!'.format(players),
                        'Playtime\'s over, {}, it\'s time to duel!'.format(players)
                                    ]))
        await asyncio.sleep(duration*60)
        
        # check if fight is still active after time ends
        if not room.active(ctx, nonce):
            return

        room.terminate(ctx, completed=True)
        await aoi.say(':clock: Aaaaand that\'s time!\n**You have three minutes to submit your results with `::fight result ##`.**')
        await asyncio.sleep(180)

        results = room.generate_results(ctx)
        if results:
            try:
                keys = sorted(results, key=results.get, reverse=True)
            except:
                print('[!] error sorting, using results as given....')
                print('results:{}'.format(results))
                keys = results
                
            formatted = ''
            print('attempting to sort with results {}'.format(results))
            for r in keys:
                formatted += '{:25.20}{}\n'.format(r.display_name, ' '.join(results[r]))
            await aoi.say(('''So hey, here are the results from the last battle:\n```{}```\n''').format(formatted) + random.choice([
                                'Thanks for playing! :star2:',
                                'Nice one!! :star2:',
                                'Good work, everybodyyy! :star2:'
                                ]))
        
    else:
        await aoi.say('Hey, one battle in here at a time, O-K?')

# cancel current battle
@fight.command(pass_context=True)
async def cancel(ctx):
    if room.active(ctx):
        room.terminate(ctx, completed=False)
        await aoi.say(random.choice(['Aw, changed your mind? Fiiiiiine ~',
                                     'Next time? I\'ll hold you to it!'
                                     ]))
    else:
        await aoi.say('There\'s no fight on here, silly.')

# join fight
@fight.command(pass_context=True)
async def join(ctx):
    if room.add_participant(ctx):
        await aoi.add_reaction(ctx.message,(random.choice(['\U0001F44D',
                                                        '\U0001F44B',
                                                        '\U0001F44F',
                                                        '\U0000270C'])))
    else:
        await aoi.say('There\'s nothing to join now. Try `::fight start`?')
# update results
@fight.command(pass_context=True)
async def result(ctx, *progress):
    if room.update_participant(ctx, progress):
        await aoi.add_reaction(ctx.message,(random.choice(['\U00002728',
                                                        '\U00002665',
                                                        '\U0001F389',
                                                        '\U0001F386'])))
        print('Progress saved for {}'.format(ctx.message.author.display_name))
    else:
        await aoi.say('There\'s nothing to update. Try `::fight start`?')


aoi.run(os.getenv('DISCORD_TOKEN'))
