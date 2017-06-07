import discord
from discord.ext import commands
from modules.parseSettings import getSettings
from modules.messageHandler import handle

botSettings = getSettings() # Get settings
client = commands.Bot(command_prefix=botSettings['prefix'], description="Bot")

@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        return # Don't let the bot reply to itself
    if not msg.content.startswith(botSettings['prefix']):
        handle(msg, client, botSettings)
        return

@client.command()
async def echo(*val : str):
    await client.say(' '.join(str(x) for x in val))
    return

client.run(botSettings['token']) # Bot token from config.yaml