import re
import random
import os
from markovgen import Markov
from classes import DiscordServer

#Function to handle messages. Uses the regex library to match certian situations.
#Randomness is to keep the bot from spamming
async def handle(msg, bot, client):

    logMessage(msg, bot) # Log the message for the markov bot

    if re.match("(spicy)", msg.content, re.IGNORECASE):
        s = random.randint(0,2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/l50LNcp.jpg")
            return

    if re.match("(obama)", msg.content, re.IGNORECASE):
        s = random.randint(0,1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/WVwEZ1b.jpg")
            return

    if re.match("(disappoint)", msg.content, re.IGNORECASE):
        s = random.randint(0,2)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/TfT8wvi.gif")
            return

    if re.match("((you.? ?r?(ar)?e)|your) wrong", msg.content, re.IGNORECASE):
        s = random.randint(0,1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/VrM58GT.jpg")
            return

    if re.match("(obligations)", msg.content, re.IGNORECASE):
        s = random.randint(0,2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/rbJTvlf.jpg")
            return

    if re.match("^(hi|hello) (waifu|bot) ?(bot)?", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "Hi {0.author.mention}".format(msg))
        return

    #if re.match("")

    if re.match("^(grr)(\s|.)?", msg.content, re.IGNORECASE):
        s = random.randint(0,4)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/FH7f5Ta.gif")
        if(s == 2):
            await client.send_message(msg.channel, "_me pats you on the head_")
        return

    if re.match("^bot be random", msg.content, re.IGNORECASE):
        if not msg.server.id in bot.markov:
            bot.markov[msg.server.id] = DiscordServer(msg.server, bot.settings, 1)
        if bot.markov[msg.server.id].markov.line_size < bot.settings['minMarkov']:
            await client.send_message(msg.channel, "Not enough data")
            return
        if not bot.markov[msg.server.id].markov == None:
            text = bot.markov[msg.server.id].markov.generate_markov_text(random.randint(6,40))
        await client.send_message(msg.channel, text)
        return

    if re.match(".*(computer|internet|server) ?.*(down|slow|broken|broke|sucks|dead)", msg.content, re.IGNORECASE):
        s = random.randint(0,1)
        if(s == 1):
            command = "fortune bofh-excuses | sed -n 3p" # Must have the bofh-excuses installed. For Ubuntu: sudo apt-get install fortune-bofh-excuses
            output = os.popen(command).read()
            output.strip()
            await client.send_message(msg.channel, output)
        return
    return


# Chat logs are stored in logs/[server_id]_chat_log
def logMessage(msg, bot):
    # If the message is broken up into two or more lines,
    # we can just replace the newline with a space
    line = msg.content.replace("\n"," ")
    if 'logNonAlphanumWords' in bot.settings and not bot.settings['logNonAlphanumWords']:
        # We don't want to log non-alphanumeric characters because something like
        # % or & or # isn't really a valuable word.
        line = re.sub("\s\W\s", " ", line)
    if 'logHttpLinks' in bot.settings and not bot.settings['logHttpLinks']:
        # If we don't want to log http links, we can remove them with regex
        line = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\s?", "", line)
    # If the message is longer than the min sentence length
    # we can process and log it 
    if len(line.split()) >= bot.settings['markovSentenceLength']:
        serverId = msg.server.id
        with open("logs/{}_chat_log".format(serverId), "a", encoding='utf-8', errors='ignore') as f:
            # Append the line to the file
            f.write("{}\n".format(line))
            # If we already have a value for this server, we don't need to make one
            if not serverId in bot.markov:
                # If the server doesn't exist in the bot markov dict yet, create it
                bot.markov[serverId] = DiscordServer(msg.server, bot.settings, 1)
            # We also can just digest the data right here and we 
            # don't have to worry about doing it later
            bot.markov[serverId].markov.digest_single_message(line)

        print("New message count for", serverId, "is",bot.markov[serverId].markov.line_size)
        print("Logged:", line)
    return