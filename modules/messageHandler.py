import re
import random
import os
from classes import DiscordServer

# Function to handle messages. Uses the regex library to match certian situations.
# Randomness is to keep the bot from spamming

# This function should contain only message responses to what users say
# It should not contain actual commands or utilities.
async def handle(msg, bot, client):
    # Log the message for the markov bot
    logMessage(msg, bot)

    if re.match(".*", msg.content, re.IGNORECASE):
        s = random.randint(0,10000)
        if(s == 42):
            n = random.randint(1,3)
            if(n == 1):
                await client.send_message(msg.channel,
                      "Here's a peek behind the scenes of me, {}: <https://www.youtube.com/watch?v=dQw4w9WgXcQ>".format(client.user.name))
            if(n == 2):
                await client.send_message(msg.channel,
                    "Perfection: <https://www.youtube.com/watch?v=dQw4w9WgXcQ>")
            if(n == 3):
                await client.send_message(msg.channel,
                    "<https://www.youtube.com/watch?v=dQw4w9WgXcQ> Obligations")

    if re.match(".*(spicy)", msg.content, re.IGNORECASE):
        s = random.randint(0, 2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/l50LNcp.jpg")
            return

    if re.match(".*(obama)", msg.content, re.IGNORECASE):
        s = random.randint(0, 1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/WVwEZ1b.jpg")
            return

    if re.match(".*(disappoint)", msg.content, re.IGNORECASE):
        s = random.randint(0, 2)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/TfT8wvi.gif")
            return

    if re.match(".*((you.? ?r?(ar)?e)|your) wrong", msg.content, re.IGNORECASE):
        s = random.randint(0, 1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/VrM58GT.jpg")
            return

    if re.match(".*(obligations)", msg.content, re.IGNORECASE):
        s = random.randint(0, 2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/rbJTvlf.jpg")
            return

    if re.match("^(hi|hello) (waifu|bot) ?(bot)?", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "Hi {0.author.mention}".format(msg))
        return

    if re.match(".*((im|i'm)|i am) (headed|going|off) ?(off)? ?(to)? (bed|sleep)", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "Good night")
        return

    if re.match("^(grr)", msg.content, re.IGNORECASE):
        s = random.randint(0, 4)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/FH7f5Ta.gif")
        if(s == 2):
            await client.send_message(msg.channel, "_{} pats you on the head_".format(client.user.name))
        return

    if re.match(".*(it.? ?i?s happening)", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "http://i.imgur.com/YtKWRKk.gif")
        return

    if re.match(".*\s(love)\s", msg.content, re.IGNORECASE):
        s = random.randint(0,8)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/AqxwFcb.jpg")
        return

    if re.match(".*(tomato)", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "http://i.imgur.com/RVgzWvi.jpg")
        return

    if re.match(".*(chrome)", msg.content, re.IGNORECASE):
        s = random.randint(0,4)
        if(s == 1):
            await client.send_message(msg.channel, "https://i.imgur.com/i9V4DKH.jpg")
        return

    if re.match(".*(iphone)", msg.content, re.IGNORECASE):
        s = random.randint(0,1)
        if(s == 1):
            await client.send_message(msg.channel, "https://i.imgur.com/rEs7rqr.jpg")
        return

    if re.match(".*\s(expect)\s", msg.content, re.IGNORECASE):
        s = random.randint(0,50)
        if(s == 42):
            await client.send_message(msg.channel, "Nobody expects the Spanish Inquisition!")
        return

    if re.match("^bot be random", msg.content, re.IGNORECASE):
        if msg.server.id not in bot.markov:
            bot.markov[msg.server.id] = DiscordServer(msg.server, bot.settings, 1)
        if bot.markov[msg.server.id].markov.line_size < bot.settings['minMarkov']:
            await client.send_message(msg.channel, "Not enough data")
            return
        if bot.markov[msg.server.id].markov is not None:
            text = bot.markov[msg.server.id].markov.generate_markov_text(random.randint(15, 40))
        await client.send_message(msg.channel, text)
        return

    if re.match(".*(computer|internet|server) ?.*(down|slow|broken|broke|sucks|dead)", msg.content, re.IGNORECASE):
        s = random.randint(0, 1)
        if(s == 1):
            # Must have the bofh-excuses installed. For Ubuntu: sudo apt-get install fortune-bofh-excuses
            command = "fortune bofh-excuses | sed -n 3p"
            output = os.popen(command).read()
            output.strip()
            await client.send_message(msg.channel, output)
        return
    return


# This function should contain what to do about direct messages
# This function is NOT for fun text replies to user messages sent in servers
async def handlePersonalMessage(msg, bot, client):
    return

# This function should contain what to do when the bot is mentioned
async def handleBotMention(msg, bot, client):
    return

# Chat logs are stored in logs/[server_id]_chat_log
def logMessage(msg, bot):
    # If the message is broken up into two or more lines,
    # we can just replace the newline with a space
    line = msg.content.replace("\n", " ")
    if 'logNonAlphanumWords' in bot.settings and not bot.settings['logNonAlphanumWords']:
        # We don't want to log non-alphanumeric characters because something like
        # % or & or # isn't really a valuable word.
        line = re.sub("\s\W\s", " ", line)
    if 'logHttpLinks' in bot.settings and not bot.settings['logHttpLinks']:
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

    # If the message is longer than the min sentence length we can process and log it
    if len(line.split()) >= bot.settings['markovSentenceLength']:
        serverId = msg.server.id
        with open("logs/{}_chat_log".format(serverId), "a", encoding='utf-8', errors='ignore') as f:
            # Append the line to the file
            f.write("{}\n".format(line))
            if serverId not in bot.markov:
                # Create server object if it doesn't exist yet
                bot.markov[serverId] = DiscordServer(msg.server, bot.settings, 0)
            # We also can just digest the data right here and we
            # don't have to worry about doing it later
            bot.markov[serverId].markov.digest_single_message(line)

        print("New message count for", serverId, "is", bot.markov[serverId].markov.line_size)
        print("Logged:", line)
    return
