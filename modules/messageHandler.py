import re
import random
import os
from markovgen import Markov
from classes import DiscordServer

#Function to handle messages. Uses the regex library to match certian situations.
#Randomness is to keep the bot from spamming
async def handle(msg, bot, client):

    logMessage(msg, bot) # Log the message for the markov bot

    if re.match(".*spicy", msg.content, re.IGNORECASE):
        s = random.randint(0,2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/l50LNcp.jpg")
            return

    if re.match(".*obama", msg.content, re.IGNORECASE):
        s = random.randint(0,1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/WVwEZ1b.jpg")
            return

    if re.match(".*disappoint", msg.content, re.IGNORECASE):
        s = random.randint(0,2)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/TfT8wvi.gif")
            return

    if re.match("((you.? ?r?(ar)?e)|your) wrong", msg.content, re.IGNORECASE):
        s = random.randint(0,1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/VrM58GT.jpg")
            return

    if re.match(".*obligations", msg.content, re.IGNORECASE):
        s = random.randint(0,2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/rbJTvlf.jpg")
            return

    if re.match("^(hi|hello) (waifu|bot) ?(bot)?", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "Hi {0.author.mention}".format(msg))
        return

    if re.match("^(grr)(\s|.)?", msg.content, re.IGNORECASE):
        s = random.randint(0,4)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/FH7f5Ta.gif")
        if(s == 2):
            await client.send_message(msg.channel, "_me pats you on the head_")
        return

    if re.match("^bot be random", msg.content, re.IGNORECASE):
        if bot.markov[msg.server.id].markovMessages < bot.settings['minMarkov']:
            await client.send_message(msg.channel, "Not enough data")
            return
        if not bot.markov[msg.server.id].markov == None:
            text = bot.markov[msg.server.id].markov.generate_markov_text(random.randint(6,40))
        await client.send_message(msg.channel, text)
        return

    if re.match(".*(computer|internet|server) .*(down|slow|broken|broke|sucks|dead)", msg.content, re.IGNORECASE):
        command = "fortune bofh-excuses | sed -n 3p" # Must have the bofh-excuses installed. For Ubuntu: sudo apt-get install fortune-bofh-excuses
        output = os.popen(command).read()
        output.strip()
        await client.send_message(msg.channel, output)
        return
    return


# Chat logs are stored in logs/[server_id]_chat_log
def logMessage(msg, bot):
    if len(msg.content.split()) > 5: # If the message is 6 words or more we log it
        serverId = msg.server.id
        with open("logs/{}_chat_log".format(serverId), "a", encoding='utf-8', errors='ignore') as f:
            f.write("{}\n".format(msg.content)) # Append the line to the file
            if serverId in bot.markov: # If we already have a value for this server, we don't need to make one
                bot.markov[serverId].markovMessages += 1 # Add 1 to message count
                if (bot.markov[serverId].markovMessages % bot.settings['markovLoad'] == 0 or 
                        bot.markov[serverId].markovMessages == bot.settings['minMarkov']): # Reload every `markovLoad` messages
                    bot.markov[serverId].markov = Markov(f, bot.settings['maxMarkovBytes']) # Do the reload
            else: # If the server doesn't exist in the bot markov dict yet, create it
                bot.markov[serverId] = DiscordServer(msg.server, bot.settings, 1)

            # We also can just digest the data right here and we don't have to worry about doing it later
            if bot.markov[serverId].markov:
                bot.markov[serverId].markov.digest_single_message(msg.content)

        #print("New message count for", serverId, "is",bot.markov[serverId].markovMessages)
        #print("Logged:", msg.content)
    return