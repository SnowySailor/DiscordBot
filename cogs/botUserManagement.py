from discord.ext import commands
import re
import discord

class BotUserManagement:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_server=True)
    async def spam(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return
        return

    @spam.group(pass_context=True)
    async def whitelist(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return
        return

    @whitelist.group(pass_context=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return
        return

    @whitelist.group(pass_context=True)
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return
        return

    @add.command(name="channel", pass_context=True)
    async def channeladd(self, ctx, cid):
        # remove <# and > from channel mention
        cid = re.sub(r"(^<#)|>", "", cid)
        if (discord.utils.get(ctx.message.server.channels, id=cid,
                type=discord.ChannelType.text) is None):
            await self.client.say("That channel isn't valid.")
            return
        serverId = ctx.message.server.id
        if cid not in self.bot.servers[serverId].whitelistChannels:
            self.bot.servers[serverId].whitelistChannels.add(cid)
            await self.client.say("Channel whitelisted.")
        else:
            await self.client.say("That channel is already whitelisted.")
        return
        return

    @add.command(name="role", pass_context=True)
    async def roleadd(self, ctx, rid):
        if rid == "@everyone" or rid == "@here":
            rid = discord.utils.get(ctx.message.server.roles, 
                name=rid)
            if rid is None:
                await self.client.say("That role doesn't exist.")
                return
            else:
                rid = rid.id
        # remove <@& and > from "<@&172688478646173696>"
        rid = re.sub(r"(^<@&)|>", "", rid)
        # Validate that the role exists
        if discord.utils.get(ctx.message.server.roles, id=rid) is None:
            await self.client.say("That role doesn't seem to be valid.")
            return
        serverId = ctx.message.server.id
        if rid not in self.bot.servers[serverId].whitelistRoles:
            self.bot.servers[serverId].whitelistRoles.add(rid)
            await self.client.say("Role whitelisted.")
        else:
            await self.client.say("That role is already whitelisted.")
        return

    @remove.command(name="channel", pass_context=True)
    async def channelremove(self, ctx, cid):
        # remove <# and > from channel mention
        cid = re.sub(r"(^<#)|>", "", cid)
        if (discord.utils.get(ctx.message.server.channels, id=cid, 
                type=discord.ChannelType.text) is None):
            await self.client.say("That channel isn't valid.")
            return
        serverId = ctx.message.server.id
        if cid in self.bot.servers[serverId].whitelistChannels:
            self.bot.servers[serverId].whitelistChannels.remove(cid)
            await self.client.say("Channel un-whitelisted.")
        else:
            await self.client.say("That channel isn't whitelisted.")
        return
        
    @remove.command(name="role", pass_context=True)
    async def roleremove(self, ctx, rid):
        # remove <@& and > from "<@&172688478646173696>"
        rid = re.sub(r"(^<@&)|>", "", rid)
        # Validate that the role exists
        if discord.utils.get(ctx.message.roles, id=rid) is None:
            await self.client.say("That role doesn't seem to be valid.")
            return
        serverId = ctx.message.server.id
        if rid in self.bot.servers[serverId].whitelistRoles:
            self.bot.servers[serverId].whitelistRoles.remove(rid)
            await self.client.say("Role un-whitelisted.")
        else:
            await self.client.say("That role isn't whitelisted.")
        return

    @whitelist.command(name="roles", pass_context=True)
    async def listroles(self, ctx):
        if len(self.bot.servers[ctx.message.server.id].whitelistRoles) is 0:
            await self.client.say("No roles whitelisted.")
            return
        li = '\n'.join("<@{}>".format(x) for x in 
            self.bot.servers[ctx.message.server.id].whitelistRoles)
        await self.client.say(li)
        return

    @whitelist.command(name="channels", pass_context=True)
    async def listchannels(self, ctx):
        if len(self.bot.servers[ctx.message.server.id].whitelistChannels) is 0:
            await self.client.say("No channels whitelisted.")
            return
        li = '\n'.join("<#{}>".format(x) for x in 
            self.bot.servers[ctx.message.server.id].whitelistChannels)
        await self.client.say(li)
        return