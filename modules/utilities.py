import re
from discord.ext import commands

def cleanMessage(msg, bot):
    serverId = msg.server.id
    # If the message is broken up into two or more lines,
    # we can just replace the newline with a space
    line = msg.content.replace("\n", " ")
    if ('removeNonAlphanumWords' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeNonAlphanumWords']):
        # We don't want to log non-alphanumeric characters because something like
        # % or & or # isn't really a valuable word.
        line = re.sub("\s\W\s", " ", line)
    if ('removeHttpLinks' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeHttpLinks']):
        # If we don't want to log http links, we can remove them with regex
        line = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\s?", "", line)
    if ('removeHereEveryone' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeHereEveryone']):
        # If we don't want @here and @everyone recorded, we can remove them
        line = re.sub("\@(here|everyone)\s", "", line)
        line = re.sub("\s\@(here|everyone)", "", line)
    if ('removeUserMentions' in bot.servers[serverId].settings['markov']
            and bot.servers[serverId].settings['markov']['removeUserMentions']):
        # If we don't want @User#Num mentions, we can remove them
        # User mentions are <@69683046830462454> in text as an example
        line = re.sub("\s?<@[0-9]+>\s", " ", line)
    return line

# Chat logs are stored in logs/[server_id]_chat_log
def logMessage(msg, bot):
    serverId = msg.server.id
    line = cleanMessage(msg, bot)

    # If the message is longer than the min sentence length we can process and log it
    lineLen = len(line.split())
    if (('markovSentenceLength' in bot.servers[serverId].settings['markov'] and
            lineLen >= bot.servers[serverId].settings['markov']['markovSentenceLength']) or
            ('markovSentenceLength' not in bot.servers[serverId].settings['markov'] and lineLen >= 5)):

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
            if (('markovDigestLength' in bot.servers[serverId].settings['markov'] and
                    lineLen >= bot.servers[serverId].settings['markov']['markovDigestLength']) or
                    ('markovDigestLength' not in bot.servers[serverId].settings['markov'])):
                bot.servers[serverId].markov.digest_single_message(line)

        print("New message count for", serverId, "is", bot.servers[serverId].markov.line_size)
        print("Logged:", line)
    return

# Use if the command requires the server to be in the DiscordBot
# def requireServer():
#     def predicate(ctx):
#         # Make sure the server exists in our bot
#         if ctx.message.server.id not in self.bot.servers:
#                self.bot.addServer(ctx.message.server,
#                                self.bot.defaultServerSettings)
#         return True
#     return commands.check(predicate)
