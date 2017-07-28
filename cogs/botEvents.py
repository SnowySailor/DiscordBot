from modules.messageHandler import handle, handlePersonalMessage, handleBotMention
from modules.messageRateLimiter import isRateLimited, handleRateLimit
from discord.ext import commands
from utilities.utilities import parse, updateKey


class BotEvents:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    async def on_message(self, msg):
        if msg.author == self.client.user or msg.author.bot:
            # Don't let the bot reply to itself and if the sender is a bot
            # then don't process that message. It could cause a loop.
            return

        # Check to see if the server is registered in the bot
        if msg.server and msg.server.id not in self.bot.servers:
            # Add a new server to the server dict.
            self.bot.addServer(msg.server, self.bot.defaultServerSettings, self.bot.defaultServerReactions)

        await self.client.process_commands(msg)

        # Server is None if the msg is a PM.
        # Use direct reference to "None" to avoid confusion
        if msg.channel.is_private:
            await handlePersonalMessage(msg, self.bot, self.client)
            return

        # Check to see if we should limit the message rate
        if ('spamFilter' in self.bot.servers[msg.server.id].settings
                and self.bot.servers[msg.server.id].settings['spamFilter']['enable']
                and isRateLimited(self.bot.redis, 
                    self.bot.servers[msg.server.id].settings, msg, bot)):
            key = msg.server.id + "." + msg.author.id
            if parse(self.bot.redis.get(key), bool) is False:
                # Set value to True to say we have handled this instance
                updateKey(self.bot.redis, key, True)
                try:
                    await handleRateLimit(self.bot, self.client, msg,
                        self.bot.servers[msg.server.id].settings['spamFilter'])
                except Exception:
                    # If the handle failed, undo the handle indication
                    updateKey(self.bot.redis, key, False)
            return

        # If the bot was mentioned directly handle that in a special way
        if msg.content.startswith("<@{}>".format(self.client.user.id)):
            await handleBotMention(msg, self.bot, self.client)
            # We don't return afterwards because it could also be a valid
            # message for handle()

        # Make sure we don't handle a message that's a command
        if not msg.content.startswith(self.bot.botSettings['prefix']):
            await handle(msg, self.bot, self.client)
            return

    async def on_ready(self):
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.bot.send_message(ctx.message.channel, "Invalid command.")
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.bot.send_message(ctx.message.channel,
                            "You can't use this command in private messages.")
        else:
            print(type(error))
        #elif isinstance(error, commands.errors.)