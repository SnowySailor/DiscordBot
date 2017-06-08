import os
from classes import DiscordBot
from discord.ext import commands
from modules.parseSettings import getSettings
from modules.messageHandler import handle

bot = DiscordBot(getSettings())
client = commands.Bot(command_prefix=bot.settings['prefix'], description="Bot")

### EVENTS ###


@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        # Don't let the bot reply to itself
        return
    if not msg.content.startswith(bot.settings['prefix']):
        await handle(msg, bot, client)
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

### COMMANDS ###


@client.command()
async def echo(*val: str):
    await client.say(' '.join(str(x) for x in val))
    return


@client.command()
async def fortune():
    command = "fortune"
    output = os.popen(command).read()
    output.strip()
    await client.say(output)
    return

#######

# Bot token from config.yaml
client.run(bot.settings['token'])
