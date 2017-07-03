import discord
from discord.ext import commands
import sys
from classes import DiscordBot

from modules.botAudio import Music
from modules.botSettings import SettingsCommands
from modules.botUtilities import UtilityCommands
from modules.botMisc import MiscCommands
from modules.botEvents import BotEvents

from modules.parseSettings import getSettings

# Perhaps there is a better way to manage this sort of thing
# TODO: Remove the defaultSettings from going into the bot,
#       make new attr that is 'token' only.
parsedSettings = getSettings()
botSettings = parsedSettings['bot']
defaultServerSettings = parsedSettings['serverSettings']

bot = DiscordBot(defaultServerSettings, botSettings)
client = commands.Bot(command_prefix=commands
                      .when_mentioned_or(bot.botSettings['prefix']), 
                      description="I am your best friend")

client.add_cog(Music(client))
client.add_cog(SettingsCommands(client, bot))
client.add_cog(UtilityCommands(client, bot))
client.add_cog(MiscCommands(client, bot))
client.add_cog(BotEvents(client, bot))

if not discord.opus.is_loaded():
    if 'opusLocation' in bot.botSettings:
        discord.opus.load_opus(bot.botSettings['opusLocation'])
    else:
        sys.exit("Failed to find opusLocation in config.yaml")

# @client.command(description="Server info")
# async def serverinfo():
#     output = os.popen('serverinfo.sh').read()
#     output.strip()
#     return output

# Bot token from config.yaml
client.run(bot.botSettings['token'])
