import re
from discord.ext import commands

def cleanMessage(line, bot):
    if 'removeNonAlphanumWords' in bot.settings and bot.settings['removeNonAlphanumWords']:
        # We don't want to log non-alphanumeric characters because something like
        # % or & or # isn't really a valuable word.
        line = re.sub("\s\W\s", " ", line)
    if 'removeHttpLinks' in bot.settings and bot.settings['removeHttpLinks']:
        # If we don't want to log http links, we can remove them with regex
        line = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\s?", "", line)
    if 'removeHereEveryone' in bot.settings and bot.settings['removeHereEveryone']:
        # If we don't want @here and @everyone recorded, we can remove them
        line = re.sub("\@(here|everyone)\s", "", line)
        line = re.sub("\s\@(here|everyone)", "", line)
    if 'removeUserMentions' in bot.settings and bot.settings['removeUserMentions']:
        # If we don't want @User#Num mentions, we can remove them
        # User mentions are <@69683046830462454> in text as an example
        line = re.sub("\s?<@[0-9]+>\s", " ", line)
    return line

# Chat logs are stored in logs/[server_id]_chat_log
def logMessage(msg, bot):
    # If the message is broken up into two or more lines,
    # we can just replace the newline with a space
    line = msg.content.replace("\n", " ")
    line = cleanMessage(line, bot)

    # If the message is longer than the min sentence length we can process and log it
    lineLen = len(line.split())
    if (('markovSentenceLength' in bot.settings and
            lineLen >= bot.settings['markovSentenceLength']) or
            ('markovSentenceLength' not in bot.settings and lineLen >= 5)):

        serverId = msg.server.id
        with open("logs/{}_chat_log".format(serverId), "a", encoding='utf-8', errors='ignore') as f:
            # Append the line to the file
            f.write("{}\n".format(line))
            if serverId not in bot.markov:
                # Create server object if it doesn't exist yet
                #bot.markov[serverId] = DiscordServer(msg.server, bot.defaultServerSettings, 0)
                bot.addServer(msg.server, bot.defaultServerSettings, 0)
            # We also can just digest the data right here and we
            # don't have to worry about doing it later
            if (('markovDigestLength' in bot.settings and
                    lineLen >= bot.settings['markovDigestLength']) or
                    ('markovDigestLength' not in bot.settings)):
                bot.markov[serverId].markov.digest_single_message(line)

        print("New message count for", serverId, "is", bot.markov[serverId].markov.line_size)
        print("Logged:", line)
    return

# Check to see if a user has the proper permissions to do something
# Takes as many permissions as necessary
def needsPermissions(*permissions):
    def predicate(ctx):
        if ctx.message.server is None:
            return False
        permissionConfirmations = []
        # Loop over the permissions we got
        for perm in permissions:
            # Check to see if the user has the permission
            ctx.message.author.server_permissions.get(perm, False)
        if not all(permissionConfirmations):
            ctx.bot.say("""You are not a server manager and cannot
                        change my settings.""")
            return all(permissionConfirmations)
    return commands.check(predicate)

# Use if the command requires the server to be in the bot
def requireServer():
    def predicate(ctx):
        # Make sure the server exists in our bot
        if ctx.message.server.id not in self.bot.servers:
            self.bot.addServer(ctx.message.server, self.bot.defaultServerSettings)
    return commands.check(predicate)