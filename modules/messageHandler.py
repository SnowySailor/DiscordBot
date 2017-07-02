import modules.messageResponder
from modules.utilities import logMessage

# This function should contain only message responses to what users say
# It should not contain actual commands or utilities.
async def handle(msg, bot, client):
    # Log the message for the markov bot
    if 'markovEnable' in bot.settings and bot.settings['markovEnable']:
        logMessage(msg, bot)

    if 'reactionsEnable' in bot.settings and bot.settings['reactionsEnable']:
        await reactToMessages(msg, bot, client)
    return


# This function should contain what to do about direct messages
# This function is NOT for fun text replies to user messages sent in servers
async def handlePersonalMessage(msg, bot, client):
    return

# This function should contain what to do when the bot is mentioned
async def handleBotMention(msg, bot, client):
    return
