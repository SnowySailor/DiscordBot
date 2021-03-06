import re
import discord
from discord.ext import commands
from classes import MagicFormatMapping, SafeFormatter
from ast import literal_eval as make_tuple

async def loadMarkovFromServer(server, bot, client):
    # Ensure that the bot has this server created
    if not server.id in bot.servers:
        return -1
    
    channelsToGet = set()
    # Loop over the channels in the server
    for channel in server.channels:
        # If the markoved channels are already loaded
        if hasattr(bot.servers[server.id], 'markoved_channels'):
            # If the channel wasn't already markoved
            if not (channel.id in bot.servers[server.id].markoved_channels):
                channelsToGet.add(channel)
        else:
            # Try to read preexisting markov channels
            if bot.servers[server.id].readFromYamlData('markoved_channels'):
                if not (channel.id in bot.servers[server.id].markoved_channels):
                    channelsToGet.add(channel)   
            else:
                # If we can't load the channels, then create a new file
                bot.servers[server.id].markoved_channels = set()
                channelsToGet.add(channel)

    for channel in channelsToGet:
        # Indicate that we've read this channel's history
        bot.servers[server.id].markoved_channels.add(channel.id)
        
        # Check the bot's permissions for the channel
        perms = server.me.permissions_in(channel)
        if not (perms.read_messages or perms.read_message_history) or channel.type is not discord.ChannelType.text:
            # We found a channel that we aren't allowed to access
            continue

        async for message in client.logs_from(channel, 500):
            if message.author == client.user or message.author.bot:
                continue
            # Log each message
            logMessage(message, bot)

    try:
        # Save the markoved channel id's to file
        bot.servers[server.id].dumpToYamlData('markoved_channels')
    except Exception as e:
        print(str(e))
        return -2

    return bot.servers[server.id].markov.line_size

def cleanMessage(msg, bot):
    serverId = msg.server.id
    # If the message is broken up into two or more lines,
    # we can just replace the newline with a space
    line = msg.content.replace("\n", " ")
    if ('removeNonAlphanumWords' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeNonAlphanumWords'][0]):
        # We don't want to log non-alphanumeric characters because something like
        # % or & or # isn't really a valuable word.
        line = re.sub("\s\W\s", " ", line)
    if ('removeHttpLinks' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeHttpLinks'][0]):
        # If we don't want to log http links, we can remove them with regex
        line = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\s?", "", line)
    if ('removeHereEveryone' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeHereEveryone'][0]):
        # If we don't want @here and @everyone recorded, we can remove them
        line = re.sub("\@(here|everyone)\s", "", line)
        line = re.sub("\s\@(here|everyone)", "", line)
    if ('removeUserMentions' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeUserMentions'][0]):
        # If we don't want @User#Num mentions, we can remove them
        # User mentions are <@69683046830462454> in text as an example
        line = re.sub("\s?<@[0-9]+>\s", " ", line)
    return line

# Chat logs are stored in logs/[server_id]_chat_log
def logMessage(msg, bot):
    serverId = msg.server.id
    line = cleanMessage(msg, bot)

    lineLen = len(line.split())
    # If the message is longer than the min sentence length we can process and log it
    if (('sentenceLength' in bot.servers[serverId].settings['markov'] and
            lineLen >= bot.servers[serverId].settings['markov']['sentenceLength'][0]) or
            ('sentenceLength' not in bot.servers[serverId].settings['markov'] and lineLen >= 5)):

        serverId = msg.server.id
        with open("logs/{}_chat_log".format(serverId), "a", encoding='utf-8', errors='ignore') as f:
            # Append the line to the file
            f.write("{}\n".format(line))
            # Should always be in the bot
            # if serverId not in bot.markov:
            #     # Create server object if it doesn't exist yet
            #     #bot.markov[serverId] = DiscordServer(msg.server, bot.defaultServerSettings, 0)
            #     bot.addServer(msg.server, bot.defaultServerSettings, 0)

            # We also can just digest the data right here and we
            # don't have to worry about doing it later
            if (('digestLength' in bot.servers[serverId].settings['markov'] and
                    lineLen >= bot.servers[serverId].settings['markov']['digestLength'][0]) or
                    ('digestLength' not in bot.servers[serverId].settings['markov'])):
                bot.servers[serverId].markov.digest_single_message(line)

        print("New message count for", serverId, "is", bot.servers[serverId].markov.line_size)
        print("Logged:", line)
    return

def parse(strVal, expectedType):
    retVal = None
    if expectedType is int:
        try:
            retVal = int(strVal)
        except ValueError:
            raise ValueError
    elif expectedType is str:
        retVal = strVal
    elif expectedType is tuple:
        try:
            retVal = make_tuple(strVal)
        except ValueError:
            raise ValueError
    elif expectedType is bool:
        if strVal.lower() == "true":
            retVal = True
        elif strVal.lower() == "false":
            retVal = False
        else:
            raise ValueError
    return retVal

def listSettings(settings, prefix=""):
    strDump = ""
    for k, v in settings.items():
        if type(v) is dict:
            strDump += listSettings(v, "{}.".format(k))
        else:
            strDump += "{}{}: {}\n".format(prefix, k, v[0])
    return strDump

# On failure throws BadArgument
def verifySetting(strVal, settings):
    if "." not in strVal:
        if strVal not in settings:
            raise commands.BadArgument
        else:
            return [strVal]
    else:
        current = settings
        chain = []

        for s in strVal.split("."):
            if s not in current:
                raise commands.BadArgument
            else:
                chain.append(s)
                current = current[s]
        return chain
    raise commands.BadArgument

def verifyReaction(strVal, reactions):
    return

# On failure throws KeyError
def setValue(storage, tree, value):
    if len(tree) == 1:
        storage[tree[0]] = value
    else:
        setValue(storage[tree[0]], tree[1:], value)

# If a key doesn't exist, returns None
def getValue(storage, tree):
    if len(tree) == 1:
        if tree[0] not in storage:
            return None
        return storage[tree[0]]
    else:
        if tree[0] not in storage:
            return None
        return getValue(storage[tree[0]], tree[1:])

# On failure throws KeyError
def deleteEntry(storage, tree):
    if len(tree) == 1:
        del storage[tree[0]]
    else:
        deleteEntry(storage[tree[0]], tree[1:])

def safe_format(_string, *args, **kwargs):
    formatter = SafeFormatter()
    kwargs = MagicFormatMapping(args, kwargs)
    return formatter.vformat(_string, args, kwargs)

def updateKey(redis, key, value):
    lua = "local pttl = redis.call('pttl', ARGV[1]) if pttl > 0 "\
        "then return redis.call('PSETEX', ARGV[1], pttl, ARGV[2]) end"
    return redis.eval(lua, 0, key, value)

def verifyAdmin(user, admins):
    if user.id in admins:
        return True
    return False

def file_to_lines(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
    return lines

def getChannelById(client, channelId):
    return client.get_channel(channelId)

async def sendMessage(client, channel, msg):
    return await client.send_message(channel, msg)


# Use if the command requires the server to be in the DiscordBot
# def requireServer():
#     def predicate(ctx):
#         # Make sure the server exists in our bot
#         if ctx.message.server.id not in self.bot.servers:
#                self.bot.addServer(ctx.message.server,
#                                self.bot.defaultServerSettings)
#         return True
#     return commands.check(predicate)
