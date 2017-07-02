from discord.ext import commands
from modules.messageHandler import handle, handlePersonalMessage, handleBotMention

class BotEvents:
    def __init__(self, client, bot):
        
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