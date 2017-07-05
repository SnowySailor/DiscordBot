import re
import random
import os
from classes import AccessData

# Handles message reactions
async def reactToMessage(msg, bot, client):

    for _, values in bot.servers[msg.server.id].reactions.items():
        reg = values[0]
        print(values)
        try:
            re.compile(reg)
        except re.error:
            await client.send_message(msg.channel, "Something is wrong with this regex: `{}`".format(reg))
            continue
        if re.match(reg, msg.content, re.IGNORECASE):
            if values[2] == 0:
                s = 0
            else:
                s = random.randint(1,values[2])
            if(s == 0):
                data = AccessData(msg.author, client.user)
                await client.send_message(msg.channel, values[1].format(data))
                return

    if re.match(".*", msg.content, re.IGNORECASE):
        s = random.randint(0, 20000)
        if(s == 42):
            n = random.randint(1, 3)
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
        s = random.randint(0, 3)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/l50LNcp.jpg")
            return

    if re.match(".*(obama)", msg.content, re.IGNORECASE):
        s = random.randint(0, 3)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/WVwEZ1b.jpg")
            return

    if re.match(".*(disappoint)", msg.content, re.IGNORECASE):
        s = random.randint(0, 4)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/TfT8wvi.gif")
            return

    if re.match(".*((you.? ?r?(ar)?e)|your) wrong", msg.content, re.IGNORECASE):
        s = random.randint(0, 1)
        if(s == 1):
            await client.send_message(msg.channel, "http://imgur.com/VrM58GT.jpg")
            return

    if re.match(".*(obligations)", msg.content, re.IGNORECASE):
        s = random.randint(0, 3)
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
        s = random.randint(0, 3)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/FH7f5Ta.gif")
        if(s == 2):
            await client.send_message(msg.channel, "_{} pats you on the head_".format(client.user.name))
        return

    if re.match(".*(it.? ?i?s happening)", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "http://i.imgur.com/YtKWRKk.gif")
        return

    if re.match(".*(love)\s", msg.content, re.IGNORECASE):
        s = random.randint(0, 10)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/AqxwFcb.jpg")
        return

    if re.match(".*(tomato)", msg.content, re.IGNORECASE):
        s = random.randint(0, 2)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/RVgzWvi.jpg")
        return

    if re.match(".*(chrome)", msg.content, re.IGNORECASE):
        s = random.randint(0, 4)
        if(s == 1):
            await client.send_message(msg.channel, "https://i.imgur.com/i9V4DKH.jpg")
        return

    if re.match(".*(iphone)", msg.content, re.IGNORECASE):
        s = random.randint(0, 3)
        if(s == 1):
            await client.send_message(msg.channel, "https://i.imgur.com/rEs7rqr.jpg")
        return

    if re.match(".*\s(expect)\s", msg.content, re.IGNORECASE):
        s = random.randint(0, 50)
        if(s == 42):
            await client.send_message(msg.channel, "Nobody expects the Spanish Inquisition!")
        return

    if re.match(".*(who is|who's) ?(the)? best (pony|waifu)\??", msg.content, re.IGNORECASE):
        await client.send_message(msg.channel, "Isn't it obvious? I'm best pony.")
        return

    if ('markovEnable' in bot.servers[msg.server.id].settings['markov'] 
            and bot.servers[msg.server.id].settings['markov']['markovEnable'] 
            and re.match("^bot be random", msg.content, re.IGNORECASE)):
        # if msg.server.id not in bot.servers:
        #     await client.send_message(msg.channel, "Loading data.")
        #     bot.addServer(msg.server, bot.defaultServerSettings)
        if (bot.servers[msg.server.id].markov.line_size < 
                bot.servers[msg.server.id].settings['markov']['minMarkov']):
            await client.send_message(msg.channel, "Not enough data.")
            return
        if bot.servers[msg.server.id].markov is not None:
            text = bot.servers[msg.server.id].markov.generate_markov_text(random.randint(15, 40))
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
