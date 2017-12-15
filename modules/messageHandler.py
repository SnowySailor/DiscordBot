from modules.messageResponder import reactToMessage
from utilities.utilities import logMessage, parse, updateKey
from modules.messageRateLimiter import isRateLimited, handleRateLimit

# This function should contain only message responses to what users say
# It should not contain actual commands or utilities.
async def handle(msg, bot, client):
    # Check to see if we should limit the message rate
    if ('spamFilter' in bot.servers[msg.server.id].settings
            and bot.servers[msg.server.id].settings['spamFilter']['enable'][0]
            and isRateLimited(bot.redis, 
                bot.servers[msg.server.id].settings, msg, bot)):
        key = msg.server.id + "." + msg.author.id
        if parse(bot.redis.get(key), bool) is False:
            # Set value to True to say we have handled this instance
            updateKey(bot.redis, key, True)
            try:
                await handleRateLimit(bot, client, msg,
                    bot.servers[msg.server.id].settings['spamFilter'])
            except Exception:
                # If the handle failed, undo the handle indication
                updateKey(bot.redis, key, False)
        return

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
async def handlePersonalMessage(msg, bot, client):
    return

# This function should contain what to do when the bot is mentioned
async def handleBotMention(msg, bot, client):
    return
