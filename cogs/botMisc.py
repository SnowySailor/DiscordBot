from discord.ext import commands
import os

class MiscCommands:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.command(description="Echo your message", no_pm=True, pass_context=True)
    async def echo(self, ctx, *val: str):
        """Echo your message"""
        msg = ctx.message
        echoMsg = await self.client.say(' '.join(str(x) for x in val))
        # Add the message id to the echo message log
        self.bot.servers[msg.server.id].echoMessages[msg.id] = echoMsg
        return


    @commands.command(description="Display a fortune from the unix `fortune` program", no_pm=True)
    async def fortune(self):
        """Display a fortune from the unix `fortune` program"""
        command = "/usr/games/fortune -e fortunes riddles literature"
        output = os.popen(command).read()
        output.strip()
        await self.client.say(output)
        return
