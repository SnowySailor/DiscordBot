from discord.ext import commands
from utilities.utilities import sendMessage, getChannelById
import os

class MiscCommands:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.command(description="Echo your message", no_pm=True, pass_context=True)
    async def echo(self, ctx, *val: str):
        """Echo your message"""
        msg = ctx.message
        toSend = ' '.join(str(x) for x in val)
        if 'botChannel' in self.bot.servers[msg.server.id].settings:
            botChan = getChannelById(self.client, self.bot.servers[msg.server.id].settings['botChannel'][0])
            if botChan.id != msg.channel.id:
                toSend = msg.author.mention + "\n" + toSend
            sentMsg = await sendMessage(self.client, botChan, toSend)
        else:
            sentMsg = await self.client.say(toSend)
        # Add the message id to the echo message log
        self.bot.servers[msg.server.id].echoMessages[msg.id] = sentMsg
        return


    @commands.command(description="Display a fortune from the unix `fortune` program", no_pm=True, pass_context=True)
    async def fortune(self, ctx, *val: str):
        msg = ctx.message
        """Display a fortune from the unix `fortune` program"""
        allowedCookies = ["fortunes", "riddles", "literature", "chucknorris", "pony"]
        toPass = []
        for s in val:
            current = s.lower().strip()
            if current in allowedCookies:
                toPass.append(current)
        if len(toPass) > 0:
            args = ' '.join(toPass)
        else:
            args = "fortunes riddles literature chucknorris pony"
        command = "/usr/games/fortune -e " + args
        output = os.popen(command).read()
        output.strip()
        toSend = output
        if 'botChannel' in self.bot.servers[msg.server.id].settings:
            botChan = getChannelById(self.client, self.bot.servers[msg.server.id].settings['botChannel'][0])
            if botChan.id != msg.channel.id:
                toSend = msg.author.mention + "\n" + toSend
            sentMsg = await sendMessage(self.client, botChan, toSend)
        else:
            sentMsg = await self.client.say(toSend)
        return
