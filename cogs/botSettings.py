from discord.ext import commands
from utilities.utilities import parse, listSettings, setValue, getValue, deleteEntry, verifySetting
import re
import copy
#from utilities.utilities import requireServer


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
        # Check to see if the setting is a valid setting from the config
        try:
            settingTree = verifySetting(setting, self.bot.defaultServerSettings)
        except commands.BadArgument:
            await self.client.say("That isn't a valid setting.")
            return
        # Check to see if the value exists in the current settings
        if getValue(self.bot.servers[server.id].settings, settingTree):
            await self.client.say("This setting is already in existance.")
            return
        print(getValue(self.bot.servers[server.id].settings, settingTree))

        # Get the type from the default settings
        (_,t) = getValue(self.bot.defaultServerSettings, settingTree)
        # Attempt to parse the setting based on the given type.
        try:
            parsedValue = parse(val, t)
        except ValueError:
            await self.client.say("Error parsing: {}\nType should be `{}`."
                                  .format(val, t))
            return
        newVal = (parsedValue, t)
        setValue(self.bot.servers[server.id].settings, settingTree, newVal)
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
        # Check to make sure the setting is already a valid setting
        try:
            settingTree = verifySetting(setting, self.bot.servers[server.id].settings)
        except commands.BadArgument:
            await self.client.say("This is not a valid setting. You can list the valid settings with `settings list`")

        # Get the previous value so that we can list it
        (oldVal, t) = getValue(self.bot.servers[server.id].settings, settingTree)
        # Attempt to parse the new value
        try:
            parsedVal = parse(newVal, t)
        except ValueError:
            await self.client.say("Error parsing: {}\nType should be `{}`."
                            .format(newVal, t))
            return
        # Check to see if the old value is the same as the new value.
        # If it is, we don't need to do anything.
        if oldVal == parsedVal:
            await self.client.say("`{}` is already the current setting for `{}`"
                            .format(oldVal, setting))
            return
        # Set the new value
        newVal = (parsedVal, t)
        setValue(self.bot.servers[server.id].settings, settingTree, newVal)
        self.bot.servers[server.id].saveSettingsState()
        await self.client.say("Setting `{}` changed from `{}` to `{}`."
                              .format(setting, oldVal, parsedVal))
        return

    @settings.command(pass_context=True, no_pm=True)
    async def remove(self, ctx, setting):
        server = ctx.message.server            
        try:
            settingsTree = verifySetting(setting, self.bot.servers[server.id].settings)
        except commands.BadArgument:
            # Can't delete a setting we don't have
            await self.client.say("This is not a setting. You can list the valid settings with `settings list`")
            return

        # Delete the setting
        deleteEntry(self.bot.servers[server.id].settings, settingsTree)
        self.bot.servers[server.id].saveSettingsState()
        await self.client.say("Setting `{}` removed.".format(setting))
        return

    @settings.command(pass_context=True, no_pm=True)
    async def reset(self, ctx):
        server = ctx.message.server
        # We need to deep copy or else updating the server settings will rewrite the defaults
        self.bot.servers[server.id].settings = copy.deepcopy(self.bot.defaultServerSettings)
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
            await self.client.say("Unrecognized mode.\n{}"
                                  .format(self.reactionsUsage()))

    @reactions.command(name="list", pass_context=True, no_pm=True)
    async def rlist(self, ctx):
        server = ctx.message.server
        settingList = "\n".join(["`{}: {}`".format(x, y) for (x,y) in
                                 self.bot.servers[server.id].reactions.items()])
        await self.client.say("Here's a list of reactions:\n{}".format(settingList))

    @reactions.command(name="add", pass_context=True, no_pm=True)
    async def radd(self, ctx, name, regex, reply, probability):
        server = ctx.message.server
        if name in self.bot.servers[server.id].reactions:
            await self.client.say("That is already a reaction. You can change it if you want!")
            return
        else:
            try:
                re.compile(regex)
            except re.error:
                await self.client.say("That regex doesn't appear to be valid.")
                return
            for _,(r,_,_) in self.bot.servers[server.id].reactions.items():
                if regex == r:
                    await self.client.say("That regex already exists.")
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

    @reactions.group(name="change", pass_context=True, no_pm=True)
    async def rchange(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return

    @rchange.command(pass_context=True, no_pm=True)
    async def reply(self, ctx, name, newVal):
        server = ctx.message.server
        if name in self.bot.servers[server.id].reactions:
            (reg,_,prob) = self.bot.servers[server.id].reactions[name]
            newTuple = (reg, newVal, prob)
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
            (_,react,prob) = self.bot.servers[server.id].reactions[name]
            newTuple = (newVal, react, prob)
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
            (reg,react,_) = self.bot.servers[server.id].reactions[name]
            newTuple = (reg, react, newVal)
            self.bot.servers[server.id].reactions[name] = newTuple
            self.bot.servers[server.id].saveReactionsState()
            await self.client.say("Updated reaction `{}`.".format(name))
        else:
            await self.client.say("This isn't a reaction. You can add it though.")
        return

    @reactions.command(name="remove", pass_context=True, no_pm=True)
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

    @reactions.command(name="reset", pass_context=True, no_pm=True)
    async def rreset(self, ctx):
        server = ctx.message.server
        self.bot.servers[server.id].reactions = copy.deepcopy(self.bot.defaultServerReactions)
        self.bot.servers[server.id].saveReactionsState()
        await self.client.say("All reactions reset to default.")


    @reactions.error
    @radd.error
    @rchange.error
    @rremove.error
    @rreset.error
    @rlist.error
    @reply.error
    @regex.error
    @probability.error
    async def reactionsError(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.client.say("You're missing some arguments.\n{}"
                                  .format(self.reactionsUsage()))
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
