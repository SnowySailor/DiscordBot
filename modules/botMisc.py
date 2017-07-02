from discord.ext import commands
import os

class MiscCommands:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.command(description="Echo your message")
    async def echo(self, *val: str):
        """Echo your message"""
        await self.client.say(' '.join(str(x) for x in val))
        return


    @commands.command(description="Display a fortune from the unix `fortune` program")
    async def fortune(self):
        """Display a fortune from the unix `fortune` program"""
        command = "fortune -e fortunes riddles literature"
        output = os.popen(command).read()
        output.strip()
        await self.client.say(output)
        return
