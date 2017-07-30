from discord.ext import commands
import discord

class BotMessenger:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.group(pass_context=True, hidden=True)
    async def sendMessage(self, ctx, channelId, msg):
        return

    @sendMessage.command(pass_context=True, hidden=True)
    async def channel(self, ctx, path, message):
        """Sends message to channel
            Usage: $sendMessage channel serverId.channelId message
        """
        try:
            serverId, channelId = path.split(".")
        except ValueError:
            # Too little/too manys arguments
            return
        return

    @sendMessage.command(pass_context=True, hidden=True)
    async def user(self, ctx, userId, message):
        """Sends message to channel
            Usage: $sendMessage user userId message
        """
        try:
            user = discord.get_user_info(userId)
        except discord.NotFound:
            # Not found
            await self.client.send_message(ctx.message.channel, "That user "\
                "doesn't exist.")
            return
        except discord.HTTPException:
            # Exception
            await self.client.send_message(ctx.message.channel, "Unexpected "\
                "error. Try again.")
            return
        try:
            await self.client.send_message(user, message)
            await self.client.send_message(ctx.message.channel, 
                "Message sent")
        except (discord.HTTPException, discord.InvalidArgument, 
                discord.NotFound):
            await self.client.send_message(ctx.message.channel, "Unexpected "\
                "error. Try again.")
            return
        except discord.Forbidden:
            await self.client.send_message(ctx.message.channel, "The bot is "\
                "unable to send a message to that user.")
            return
        return