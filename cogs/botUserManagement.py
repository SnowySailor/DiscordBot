from discord.ext import commands
import re

class BotUserManagement:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_server=True)
    async def spam(self, ctx):
        return

    @spam.group(pass_context=True)
    async def whitelist(self, ctx):
        return

    @whitelist.group(pass_context=True)
    async def list(self, ctx):
        return

    @whitelist.group(pass_context=True)
    async def channel(self, ctx):
        return

    @whitelist.group(pass_context=True)
    async def role(self, ctx):
        return

    @channel.comand(pass_context=True)
    async def add(self, ctx, cid):
        # remove <# and > from channel mention
        cid = re.sub(r"(^<#)|>", "", cid)
        chan = ctx.message.channel
        if (discord.utils.get(ctx.message.server.channels, id=cid, 
                type=discord.ChannelType.text) is None):
            await self.client.send_message(chan, "That channel isn't valid.")
            return
        serverId = ctx.message.server.id
        if cid not in bot.servers[serverId].whitelistChannels:
            self.bot.servers[serverId].whitelistChannels.add(cid)
            await self.client.send_message(chan, "Channel whitelisted.")
        else:
            await self.client.send_message(chan, "That channel is already "\
                "whitelisted.")
        return
        return

    @role.command(name="add", pass_context=True)
    async def roleadd(self, ctx, rid):
        # remove <@& and > from "<@&172688478646173696>"
        rid = re.sub(r"(^<@&)|>", "", rid)
        chan = ctx.message.channel
        # Validate that the role exists
        if discord.utils.get(ctx.message.roles, id=rid) is None:
            await self.client.send_message(chan, "That role doesn't seem to "\
                "be valid.")
            return
        serverId = ctx.message.server.id
        if rid not in self.bot.servers[serverId].whitelistRoles:
            self.bot.servers[serverId].whitelistRoles.add(rid)
            await self.client.send_message(chan, "Role whitelisted.")
        else:
            await self.client.send_message(chan, "That role is already "\
                "whitelisted.")
        return

    @channel.comand(pass_context=True)
    async def remove(self, ctx, cid):
        # remove <# and > from channel mention
        cid = re.sub(r"(^<#)|>", "", cid)
        chan = ctx.message.channel
        if (discord.utils.get(ctx.message.server.channels, id=cid, 
                type=discord.ChannelType.text) is None):
            await self.client.send_message(chan, "That channel isn't valid.")
            return
        serverId = ctx.message.server.id
        if cid in bot.servers[serverId].whitelistChannels:
            self.bot.servers[serverId].whitelistChannels.remove(cid)
            await self.client.send_message(chan, "Channel un-whitelisted.")
        else:
            await self.client.send_message(chan, "That channel isn't "\
                "whitelisted.")
        return
        
    @role.command(name="remove", pass_context=True)
    async def roleremove(self, ctx, rid):
        # remove <@& and > from "<@&172688478646173696>"
        rid = re.sub(r"(^<@&)|>", "", rid)
        chan = ctx.message.channel
        # Validate that the role exists
        if discord.utils.get(ctx.message.roles, id=rid) is None:
            await self.client.send_message(chan, "That role doesn't seem to "\
                "be valid.")
            return
        serverId = ctx.message.server.id
        if rid in self.bot.servers[serverId].whitelistRoles:
            self.bot.servers[serverId].whitelistRoles.remove(rid)
            await chan.send_message("Role un-whitelisted.")
        else:
            await self.client.send_message(chan, "That role isn't whitelisted.")
        return