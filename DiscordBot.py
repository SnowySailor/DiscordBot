import os
from classes import DiscordBot
from discord.ext import commands
from modules.parseSettings import getSettings
from modules.messageHandler import handle, handlePersonalMessage, handleBotMention

bot = DiscordBot(getSettings())
client = commands.Bot(command_prefix=commands.when_mentioned_or(bot.settings['prefix']), description="Bot")

### EVENTS ###


@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        # Don't let the bot reply to itself
        return

    # Server is None if the msg is a PM.
    # Use direct reference to "None" to avoid confusion
    if msg.server == None:
        await handlePersonalMessage(msg, bot, client)
        return

    # If the bot was mentioned directly handle that in a special way
    if msg.content.startswith("<@{}>".format(client.user.id)):
        await handleBotMention(msg, bot, client)
        # We don't return afterwards because it could also be a valid
        # message for handle()

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


@client.command(description="Echo your message")
async def echo(*val: str):
    """Echo your message"""
    await client.say(' '.join(str(x) for x in val))
    return


@client.command(description="Display a fortune from the unix `fortune` program")
async def fortune():
    """Display a fortune from the unix `fortune` program"""
    command = "fortune -e fortunes riddles literature"
    output = os.popen(command).read()
    output.strip()
    await client.say(output)
    return

#######

# Bot token from config.yaml
client.run(bot.settings['token'])
