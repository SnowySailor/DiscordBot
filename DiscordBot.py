import os
import asyncio
import itertools
import random
import string
from threading import Timer
from classes import DiscordBot, TimeDenum
from discord.ext import commands
from modules.parseSettings import getSettings
from modules.messageHandler import handle, handlePersonalMessage, handleBotMention

bot = DiscordBot(getSettings())
client = commands.Bot(command_prefix=commands.when_mentioned_or(bot.settings['prefix']), description="Bot")

### EVENTS ###


@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        # Don't let the bot reply to itself
        return

    # Server is None if the msg is a PM.
    # Use direct reference to "None" to avoid confusion
    if msg.server == None:
        await handlePersonalMessage(msg, bot, client)
        return

    # If the bot was mentioned directly handle that in a special way
    if msg.content.startswith("<@{}>".format(client.user.id)):
        await handleBotMention(msg, bot, client)
        # We don't return afterwards because it could also be a valid
        # message for handle()

    if not msg.content.startswith(bot.settings['prefix']):
        await handle(msg, bot, client)
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

### COMMANDS ###


@client.command(description="Echo your message")
async def echo(*val: str):
    """Echo your message"""
    await client.say(' '.join(str(x) for x in val))
    return


@client.command(description="Display a fortune from the unix `fortune` program")
async def fortune():
    """Display a fortune from the unix `fortune` program"""
    command = "fortune -e fortunes riddles literature"
    output = os.popen(command).read()
    output.strip()
    await client.say(output)
    return

@client.command(pass_context=True)
async def timer(ctx, time=None, name=None):
    """Sets a timer. Usage: timer XhYmZs [NAME]"""
    def timerUsage():
        return ("Usage: `timer XhYmZs [NAME]`\n"+
                "Quotes also work: \"5 minutes 30 seconds\"")

    def convertToSeconds(value, desc):
        if desc == TimeDenum.S:
            return value
        if desc == TimeDenum.M:
            return value*60
        if desc == TimeDenum.H:
            return value*3600

    if not time:
        await client.say("Not enough arguments.\n{}".format(timerUsage()))
        return

    validTimes = {'seconds': TimeDenum.S, 'second': TimeDenum.S, 
                  'sec': TimeDenum.S, 's': TimeDenum.S, 'min': TimeDenum.M, 
                  'minutes': TimeDenum.M, 'minute': TimeDenum.M,'m': TimeDenum.M, 
                  'hours': TimeDenum.H, 'hour': TimeDenum.H, 'h': TimeDenum.H}
    callingUser = ctx.message.author.id
    timeSplit = [("".join(x)).strip() for _, x in itertools.groupby(time, key=str.isdigit)]
    timeNum = 0
    print(timeSplit)
    try:
        timeNum = int(timeSplit[0])
    except ValueError:
        await client.say("Unrecognized time: {}\n{}".format(
                         time, timerUsage()))
        return
    if len(timeSplit) > 1:
        timeNum = 0
        count = 0
        add = 0
        desc = ""
        while count < len(timeSplit):
            try:
                add = int(timeSplit[count])
            except ValueError:
                await client.say("Unrecognized time: {}\n{}".format(
                                 time, timerUsage()))
                return
            if count+1 < len(timeSplit):
                desc = timeSplit[count+1]
                if desc.lower() in validTimes:
                    timeNum += convertToSeconds(add, validTimes[desc.lower()])
                else:
                    await client.say("Unrecognized time multiplier: {}\n{}"
                                     .format(desc, timerUsage()))
                    return
            else:
                await client.say("Unexpected time termination: {}\n{}"
                                 .format(time, timerUsage()))
                return
            count += 2
        
    expireTime = "{} seconds".format(timeNum)
    if not name:
        # Requires Python 3.6+
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    if 'maxTimerSeconds' in bot.settings and timeNum > bot.settings['maxTimerSeconds']:
        await client.say("The time requested is too much. Please use a smaller number.")
        return
    await client.say("Timer called `{}` started. It will expire in {}.".format(name, expireTime))
    await asyncio.sleep(timeNum)
    await client.say("<@{}> Timer `{}` expired.".format(callingUser, name))
    return

#######

# Bot token from config.yaml
client.run(bot.settings['token'])
