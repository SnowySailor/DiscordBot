import logging
import os
import discord
from discord.ext import commands
from modules.parseSettings import getSettings
from modules.messageHandler import handle

class DiscordBot:
    def __init__(self, settings):
        self.markov = None
        self.settings = settings

bot = DiscordBot(getSettings())
client = commands.Bot(command_prefix=bot.settings['prefix'], description="Bot")

@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        return # Don't let the bot reply to itself
    if not msg.content.startswith(bot.settings['prefix']):
        await handle(msg, bot, client)
        return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def echo(*val : str):
    await client.say(' '.join(str(x) for x in val))
    return

@client.command()
async def fortune():
    command = "/usr/games/fortune bofh-excuses | sed -n 3p"
    output = os.popen(command).read()
    output.strip()
    await client.say(output)
    return

client.run(bot.settings['token']) # Bot token from config.yaml