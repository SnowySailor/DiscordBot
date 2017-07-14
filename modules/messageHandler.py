from modules.messageResponder import reactToMessage
from modules.messageRateLimiter import isRateLimited
from utilities.utilities import logMessage
from classes import DiscordBot

# This function should contain only message responses to what users say
# It should not contain actual commands or utilities.
async def handle(msg, bot, client):
    # Log the message for the markov bot
    serverId = msg.server.id
    if ('enable' in bot.servers[serverId].settings['markov'] and 
            bot.servers[serverId].settings['markov']['enable'][0]):
        logMessage(msg, bot)

    if ('reactionsEnable' in bot.servers[serverId].settings and 
            bot.servers[serverId].settings['reactionsEnable'][0]):
        await reactToMessage(msg, bot, client)
    return


# This function should contain what to do about direct messages
# This function is NOT for fun text replies to user messages sent in servers
async def handlePersonalMessage(msg, bot, client):
    return

# This function should contain what to do when the bot is mentioned
async def handleBotMention(msg, bot, client):
    return
