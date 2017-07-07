from discord.ext import commands
from modules.utilities import parse, listSettings, setValue, getValue, verifySetting
import re
#from modules.utilities import requireServer


class SettingsCommands:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    def settingsUsage(self):
        return ("""Usage: 
                `settings change SETTING NEWVAL`
                `settings list`
                `settings add SETTING VAL`
                `settings remove SETTING`
                `settings reset` **(reset!)**""")

    def reactionsUsage(self):
        return ("""Usage: 
                `reactions change [regex|reply|probability] NAME NEWVALUE`
                `reactions list`
                `reactions add NAME REGEX REPLY PROBABILITY`
                `reactions remove NAME`
                `reactions reset` **(reset!)**""")

    @commands.group(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_server=True)
    #@requireServer
    async def settings(self, ctx):
        """Allows changing of server settings"""
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return

    @settings.command(pass_context=True, no_pm=True)
    async def add(self, ctx, setting, val):
        server = ctx.message.server
        if setting in self.bot.servers[server.id].settings:
            # Setting is already in use
            await self.client.say("""That is already a setting. You can modify it or remove it:""")
            return
        else:
            # This is a new setting
            self.bot.servers[server.id].settings[setting][0] = val
            self.bot.servers[server.id].saveSettingsState()
            await self.client.say("Setting `{}` added with value `{}`"
                            .format(setting, val))
            return

    @settings.command(pass_context=True, no_pm=True)
    async def list(self, ctx):
        server = ctx.message.server
        # Embed message perhaps
        await self.client.say("Here is a list of settings:\n{}"
                              .format(listSettings(self.bot.servers[server.id].settings)))
        return

    @settings.command(pass_context=True, no_pm=True)
    async def change(self, ctx, setting, newVal):
        server = ctx.message.server

        try:
            settingTree = verifySetting(setting, self.bot.servers[server.id].settings)
        except commands.BadArgument:
            await self.client.say("This is not a valid setting. You can list the valid settings with `settings list`")

        oldVal = getValue(self.bot.servers[server.id].settings, settingTree)
        t = oldVal[1]
        try:
            parsedVal = parse(newVal, t)
        except ValueError:
            await self.client.say("Error parsing: {}\nType should be `{}`."
                            .format(newVal, t))
            return

        if oldVal[0] == parsedVal:
            await self.client.say("`{}` is already the current setting for `{}`"
                            .format(oldVal[0], setting))
            return

        newVal = (parsedVal, t)
        setValue(self.bot.servers[server.id].settings, settingTree, newVal)
        self.bot.servers[server.id].saveSettingsState()
        await self.client.say("Setting `{}` changed from `{}` to `{}`."
                              .format(setting, oldVal[0], newVal[0]))
        return

    @settings.command(pass_context=True, no_pm=True)
    async def remove(self, ctx, setting):
        server = ctx.message.server
        if setting not in self.bot.servers[server.id].settings:
            # Can't delete a setting we don't have
            await self.client.say("""This is not a valid setting. You can list the valid settings with `settings list`""")
            return
        else:
            # Delete the setting
            oldVal = self.bot.servers[server.id].settings[setting][0]
            del self.bot.servers[server.id].settings[setting]
            self.bot.servers[server.id].saveSettingsState()
            await self.client.say("Setting `{}` removed.".format(setting))
            return

    @settings.command(pass_context=True, no_pm=True)
    async def reset(self, ctx):
        server = ctx.message.server
        self.bot.servers[server.id].settings = self.bot.defaultServerSettings
        self.bot.servers[server.id].saveSettingsState()
        await self.client.say("All settings reset to default.")

    @settings.error
    @add.error
    @change.error
    @remove.error
    @reset.error
    @list.error
    async def settingsError(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.client.say("You're missing some arguments.\n{}".format(self.settingsUsage()))
            return
        elif isinstance(error, commands.NoPrivateMessage):
            await self.client.say("You can't call this from direct messages!")
            return
        elif isinstance(error, commands.CheckFailure):
            await self.client.say("Sorry, you don't have the Manage Server permission.")
            return
        elif isinstance(error, commands.TooManyArguments):
            await self.client.say("There's too many arguments. Please make sure you called the command correctly.\n{}"
                                  .format(self.settingsUsage()))
            return
        elif isinstance(error, commands.BadArgument):
            await self.client.say("There seems to be a bad argument.\n{}"
                                  .format(self.settingsUsage()))
            return

    # TODO: Write
    @commands.group(pass_context=True, no_pm=True)
    @commands.has_permissions(manage_server=True)
    #@requireServer
    async def reactions(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.client.say("Unrecognized modification mode.\n{}"
                                  .format(self.reactionsUsage()))

    @reactions.command(pass_context=True, no_pm=True, aliases=['list'])
    async def rlist(self, ctx):
        server = ctx.message.server
        settingList = "\n".join(["`{}: {}`".format(x, y) for (x,y) in
                                 self.bot.servers[server.id].reactions.items()])
        await self.client.say("Here's a list of reactions:\n{}".format(settingList))

    @reactions.command(pass_context=True, no_pm=True, aliases=['add'])
    async def radd(self, ctx, name, regex, reply, probability):
        server = ctx.message.server
        if name in self.bot.servers[server.id].reactions:
            await client.say("That is already a reaction. You can change it if you want!")
            return
        else:
            try:
                re.compile(regex)
            except re.error:
                await self.client.say("That regex doesn't appear to be valid.")
                return
            try:
                probability = int(probability)
            except ValueError:
                await self.client.say("Your probability must be an integer.")
                return
            self.bot.servers[server.id].reactions[name] = (regex, reply, probability)
            self.bot.servers[server.id].saveReactionsState()
            await self.client.say("Reaction `{}` added.".format(name))
            return

    @reactions.group(pass_context=True, no_pm=True, aliases=['change'])
    async def rchange(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return

    @rchange.command(pass_context=True, no_pm=True)
    async def reaction(self, ctx, name, newVal):
        server = ctx.message.server
        if name in self.bot.servers[server.id].reactions:
            oldTuple = self.bot.servers[server.id].reactions[name]
            newTuple = (newVal, oldTuple[1], oldTuple[2])
            self.bot.servers[server.id].reactions[name] = newTuple
            self.bot.servers[server.id].saveReactionsState()
            await self.client.say("Updated reaction `{}`.".format(name))
        else:
            await self.client.say("This isn't a reaction. You can add it though.")
        return

    @rchange.command(pass_context=True, no_pm=True)
    async def regex(self, ctx, name, newVal):
        server = ctx.message.server
        if name in self.bot.servers[server.id].reactions:
            try:
                re.compile(newVal)
            except re.error:
                await self.client.say("That regex doesn't appear to be valid.")
                return
            oldTuple = self.bot.servers[server.id].reactions[name]
            newTuple = (oldTuple[0], newVal, oldTuple[2])
            self.bot.servers[server.id].reactions[name] = newTuple
            self.bot.servers[server.id].saveReactionsState()
            await self.client.say("Updated reaction `{}`.".format(name))
        else:
            await self.client.say("This isn't a reaction. You can add it though.")
        return

    @rchange.command(pass_context=True, no_pm=True)
    async def probability(self, ctx, name, newVal):
        server = ctx.message.server
        if name in self.bot.servers[server.id].reactions:
            try:
                newVal = int(newVal)
            except ValueError:
                await self.client.say("Your probability must be an integer.")
                return
            oldTuple = self.bot.servers[server.id].reactions[name]
            newTuple = (oldTuple[0], oldTuple[1], newVal)
            self.bot.servers[server.id].reactions[name] = newTuple
            self.bot.servers[server.id].saveReactionsState()
            await self.client.say("Updated reaction `{}`.".format(name))
        else:
            await self.client.say("This isn't a reaction. You can add it though.")
        return

    @reactions.command(pass_context=True, no_pm=True, aliases=['remove'])
    async def rremove(self, ctx, name):
        server = ctx.message.server
        if name not in self.bot.servers[server.id].reactions:
            await self.client.say("That isn't a reaction. You can list them with `reactions list`")
            return
        else:
            oldVal = self.bot.servers[server.id].reactions[name]
            del self.bot.servers[server.id].reactions[name]
            self.bot.servers[server.id].saveReactionsState()
            await self.client.say("Reaction {} with value {} removed."
                                  .format(name, oldVal))
            return

    @reactions.command(pass_context=True, no_pm=True, aliases=['reset'])
    async def rreset(self, ctx):
        server = ctx.message.server
        self.bot.servers[server.id].reactions = self.bot.defaultServerReactions
        self.bot.servers[server.id].saveReactionsState()
        await self.client.say("All reactions reset to default.")


    @reactions.error
    @radd.error
    @rchange.error
    @rremove.error
    @rreset.error
    @rlist.error
    @reaction.error
    @regex.error
    @probability.error
    async def reactionsError(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.client.say("You're missing some arguments.\n{}".format(self.reactionsUsage()))
            return
        elif isinstance(error, commands.NoPrivateMessage):
            await self.client.say("You can't call this from direct messages!")
            return
        elif isinstance(error, commands.CheckFailure):
            await self.client.say("Sorry, you don't have the Manage Server permission.")
            return
        elif isinstance(error, commands.TooManyArguments):
            await self.client.say("There's too many arguments. Please make sure you called the command correctly.\n{}"
                                  .format(self.reactionsUsage()))
            return
        elif isinstance(error, commands.BadArgument):
            await self.client.say("There seems to be a bad argument.\n{}"
                                  .format(self.reactionsUsage()))
            return
