from discord.ext import commands
import discord
from utilities.utilities import verifyAdmin

class BotMessenger:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.group(pass_context=True, hidden=True)
    async def sendMessage(self, ctx):
        """Sends a message to a user or channel.
            Type `$help sendMessage` for more info
        """
        return

    @sendMessage.command(pass_context=True, hidden=True)
    async def channel(self, ctx, channelId, message):
        """Sends message to channel
            Usage: `$sendMessage channel channelId message`
        """
        if not verifyAdmin(ctx.message.author,
                self.bot.botSettings['botAdmins']):
            print("Bad access: {}".format(ctx.message.author.id))
            return
        chan = self.client.get_channel(channelId)
        if chan is None:
            await self.client.say("That channel doesn't exist.")
            return
        else:
            try:
                await self.client.send_message(chan, message)
                await self.client.say("Message sent.")
            except (discord.HTTPException, discord.InvalidArgument, 
                discord.NotFound) as e:
                await self.client.say("Unexpected error. Try again.")
                return
            except discord.Forbidden:
                await self.client.say("The bot is unable to send a message "\
                    "to that channel.")
                return
        return

    @sendMessage.command(pass_context=True, hidden=True)
    async def user(self, ctx, userId, message):
        """Sends message to channel
            Usage: `$sendMessage user userId message`
        """
        if not verifyAdmin(ctx.message.author, 
                self.bot.botSettings['botAdmins']):
            print("Bad access: {}".format(ctx.message.author.id))
            return
        try:
            user = await self.client.get_user_info(userId)
        except discord.NotFound:
            # Not found
            await self.client.say("That user doesn't exist.")
            return
        except discord.HTTPException:
            # Exception
            await self.client.say("Unexpected error. Try again.")
            return
        try:
            await self.client.send_message(user, message)
            await self.client.say("Message sent")
        except (discord.HTTPException, discord.InvalidArgument, 
                discord.NotFound) as e:
            await self.client.say("Unexpected error. Try again.")
            return
        except discord.Forbidden:
            await self.client.say("The bot is unable to send a message to "\
                "that user.")
            return
        return
