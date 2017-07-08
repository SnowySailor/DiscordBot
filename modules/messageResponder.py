import re
import random
import os
from classes import AccessData
from modules.utilities import safe_format

# Handles message reactions
async def reactToMessage(msg, bot, client):
    for _, (reg,reply,prob) in bot.servers[msg.server.id].reactions.items():
        try:
            re.compile(reg)
        except re.error:
            await client.send_message(msg.channel, "Something is wrong with this regex: `{}`".format(reg))
            continue
        if re.match(reg, msg.content, re.IGNORECASE):
            if prob == 0:
                s = 1
            else:
                s = random.randint(1,prob)
            if(s == 1):
                data = AccessData(msg.author, client.user)
                try:
                    await client.send_message(msg.channel, safe_format(reply, data))
                except AttributeError:
                    await client.send_message(msg.channel, "Something is fishy with this reply: `{}`"
                        .format(reply))
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

    if re.match("^(grr)", msg.content, re.IGNORECASE):
        s = random.randint(0, 3)
        if(s == 1):
            await client.send_message(msg.channel, "http://i.imgur.com/FH7f5Ta.gif")
        if(s == 2):
            await client.send_message(msg.channel, "_{} pats you on the head_".format(client.user.name))
        return

    if ('markovEnable' in bot.servers[msg.server.id].settings['markov'] 
            and bot.servers[msg.server.id].settings['markov']['markovEnable'][0] 
            and re.match("^bot be random", msg.content, re.IGNORECASE)):
        if (bot.servers[msg.server.id].markov.line_size < 
                bot.servers[msg.server.id].settings['markov']['minMarkov'][0]):
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
