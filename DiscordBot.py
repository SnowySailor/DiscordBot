import discord
from discord.ext import commands
import sys
from classes import DiscordBot

from modules.botAudio import Music
from modules.botSettings import SettingsCommands
from modules.botUtilities import UtilityCommands
from modules.botMisc import MiscCommands

from modules.parseSettings import getSettings
from modules.messageHandler import handle, handlePersonalMessage, handleBotMention

# Perhaps there is a better way to manage this sort of thing
# TODO: Remove the defaultSettings from going into the bot,
#       make new attr that is 'token' only.
defaultSettings = getSettings()
defaultServerSettings = [(k,v) for (k,v) in defaultSettings if k != 'token']
bot = DiscordBot(defaultSettings)
client = commands.Bot(command_prefix=commands.when_mentioned_or(bot.settings['prefix']), 
                      description="I am your best friend")
client.add_cog(Music(client))
client.add_cog(SettingsCommands(client, bot))
client.add_cog(UtilityCommands(client, bot))
client.add_cog(MiscCommands(client, bot))

if not discord.opus.is_loaded():
    if 'opusLocation' in bot.settings:
        discord.opus.load_opus(bot.settings['opusLocation'])
    else:
        sys.exit("Failed to find opusLocation in config.yaml")

### EVENTS ###


@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user or msg.author.bot:
        # Don't let the bot reply to itself and if the sender is a bot
        # then don't process that message. It could cause a loop.
        return

    # Server is None if the msg is a PM.
    # Use direct reference to "None" to avoid confusion
    if msg.server is None:
        await handlePersonalMessage(msg, bot, client)
        return

    # Check to see if the server is registered in the bot
    if msg.server.id not in bot.servers:
        # Add a new server to the server dict.
        #bot.servers[msg.server.id] = DiscordServer(msg.server, bot.defaultServerSettings)
        bot.addServer(msg.server, bot.defaultServerSettings)

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

# @client.command(description="Server info")
# async def serverinfo():
#     output = os.popen('serverinfo.sh').read()
#     output.strip()
#     return output

#######

# Bot token from config.yaml
client.run(bot.settings['token'])
