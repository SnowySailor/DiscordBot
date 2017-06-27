import os
import asyncio
import itertools
import random
import string
import discord
import sys
from classes import DiscordBot, TimeDenum, Music
from discord.ext import commands
from modules.parseSettings import getSettings
from modules.messageHandler import handle, handlePersonalMessage, handleBotMention

# Perhaps there is a better way to manage this sort of thing
# TODO: Remove the defaultSettings from going into the bot,
#       make new attr that is 'token' only.
defaultSettings = getSettings()
defaultServerSettings = [(k,v) for (k,v) in defaultSettings if k != 'token']
bot = DiscordBot(defaultSettings)
client = commands.Bot(command_prefix=commands.when_mentioned_or(bot.settings['prefix']), 
                      description="I am your best friend")
client.add_cog(Music(client))

if not discord.opus.is_loaded():
    if 'opusLocation' in bot.settings:
        discord.opus.load_opus(bot.settings['opusLocation'])
    else:
        sys.exit("Failed to find opusLocation in config.yaml")

### EVENTS ###


@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user or msg.author.bot:
        # Don't let the bot reply to itself and if the sender is a bot
        # then don't process that message. It could cause a loop.
        return

    # Server is None if the msg is a PM.
    # Use direct reference to "None" to avoid confusion
    if msg.server == None:
        await handlePersonalMessage(msg, bot, client)
        return

    # Check to see if the server is registered in the bot
    if msg.server.id not in bot.servers:
        # Add a new server to the server dict.
        #bot.servers[msg.server.id] = DiscordServer(msg.server, bot.defaultServerSettings)
        bot.addServer(msg.server, bot.defaultServerSettings)

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

@client.command(pass_context=True, no_pm=True)
async def modifySetting(ctx, mode=None, setting=None, newVal=None):
    """Allows changing of server settings"""
    def modifyUsage():
        return ("Usage: `modifySetting change SETTING NEWVAL`\n"+
                "`modifySetting list` to list settings\n"+
                "`modifySetting add SETTING VAL`\n"+
                "`modifySetting remove SETTING`\n")
    server = ctx.message.server

    # Permissions check
    # TODO: Allow admins to specify roles that can change bot settings
    # MAYBE TODO: If role is updated, give server admin a warning
    if not ctx.message.author.administrator:
        client.say("You are not an administrator and cannot change my settings.")
        return
    # Make sure the server exists in our bot
    if server.id not in bot.servers:
        #bot.servers[server.id] = DiscordServer(server, bot.defaultServerSettings)
        bot.addServer(server, bot.defaultServerSettings)

    if mode.lower() == "list":
        settingList = "\n".join(["`{}`".format(x) for x in bot.servers[server.id].keys()])
        client.say("Here is a list of settings:\n{}".format(settingList))
        return

    if not setting or not newVal:
        client.say(modifyUsage())
        return

    if mode.lower() == "add":
        if setting in bot.server[server.id].settings:
            # Setting is already in use
            client.say("That is already a setting. You can modify it or remove it:\n{}"
                       .format(modifyUsage()))
            return
        else
            # This is a new setting
            bot.servers[server.id].settings[setting] = newVal
            bot.servers[server.id].saveSettingsState()
            client.say("Setting `{}` added with value `{}`"
                       .format(setting, newVal))
            return

    if mode.lower() == "change":
        if setting not in bot.servers[server.id].settings:
            # This is not a setting yet
            client.say("This is not a valid setting. You can list the valid settings with `modifySetting list`")
            return
        else
            # This is a setting we can change
            oldVal = bot.servers[server.id].settings[setting]
            bot.servers[server.id].settings[setting] = newVal
            bot.servers[server.id].settings.saveSettingsState()
            client.say("Setting `{}` changed from `{}` to `{}`."
                       .format(setting, oldVal, newVal))
            return

    if mode.lower() == "remove":
        if setting not in bot.servers[server.id].settings:
            # Can't delete a setting we don't have
            client.say("This is not a valid setting. You can list the valid settings with `modifySetting list`")
            return
        else
            # Delete the setting
            oldVal = bot.servers[server.id].settings[setting]
            del bot.servers[server.id].settings[setting]
            bot.servers[server.id].saveSettingsState()
            client.say("Setting `{}` removed.")
            return

    return

# TODO: Write
@client.command(pass_context=True, no_pm=True)
async def modifyReaction(ctx, reaction=None, regex=None, reply=None):
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

# @client.command(description="Server info")
# async def serverinfo():
#     output = os.popen('serverinfo.sh').read()
#     output.strip()
#     return output

#######

# Bot token from config.yaml
client.run(bot.settings['token'])
