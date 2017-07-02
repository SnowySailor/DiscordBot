from classes import TimeDenum
from discord.ext import commands
import itertools
import string
import random
import asyncio


class UtilityCommands:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.command(pass_context=True)
    async def timer(self, ctx, time=None, name=None):
        """Sets a timer. Usage: timer XhYmZs [NAME]"""
        def timerUsage():
            return ("Usage: `timer XhYmZs [NAME]`\n"+
                    "Quotes also work: \"5 minutes 30 seconds\"")

        def convertToSeconds(value, desc):
            if desc == TimeDenum.S:
                return value
            if desc == TimeDenum.M:
                return value*60
            if desc == TimeDenum.H:
                return value*3600

        if not time:
            await self.client.say("Not enough arguments.\n{}".format(timerUsage()))
            return

        validTimes = {'seconds': TimeDenum.S, 'second': TimeDenum.S, 
                      'sec': TimeDenum.S, 's': TimeDenum.S, 'min': TimeDenum.M, 
                      'minutes': TimeDenum.M, 'minute': TimeDenum.M,'m': TimeDenum.M, 
                      'hours': TimeDenum.H, 'hour': TimeDenum.H, 'h': TimeDenum.H}
        callingUser = ctx.message.author.id
        timeSplit = [("".join(x)).strip() for _, x in itertools.groupby(time, key=str.isdigit)]
        timeNum = 0
        print(timeSplit)
        try:
            timeNum = int(timeSplit[0])
        except ValueError:
            await self.client.say("Unrecognized time: {}\n{}".format(
                             time, timerUsage()))
            return
        if len(timeSplit) > 1:
            timeNum = 0
            count = 0
            add = 0
            desc = ""
            while count < len(timeSplit):
                try:
                    add = int(timeSplit[count])
                except ValueError:
                    await self.client.say("Unrecognized time: {}\n{}".format(
                                     time, timerUsage()))
                    return
                if count+1 < len(timeSplit):
                    desc = timeSplit[count+1]
                    if desc.lower() in validTimes:
                        timeNum += convertToSeconds(add, validTimes[desc.lower()])
                    else:
                        await self.client.say("Unrecognized time multiplier: {}\n{}"
                                         .format(desc, timerUsage()))
                        return
                else:
                    await self.client.say("Unexpected time termination: {}\n{}"
                                     .format(time, timerUsage()))
                    return
                count += 2
        # TODO: Format in more useful way
        expireTime = "{} seconds".format(timeNum)
        if not name:
            # Requires Python 3.6+
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if 'maxTimerSeconds' in self.bot.settings and timeNum > self.bot.settings['maxTimerSeconds']:
            await self.client.say("The time requested is too much. Please use a smaller number.")
            return
        await self.client.say("Timer called `{}` started. It will expire in {}.".format(name, expireTime))
        await asyncio.sleep(timeNum)
        await self.client.say("<@{}> Timer `{}` expired.".format(callingUser, name))
        return
