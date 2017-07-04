from discord.ext import commands
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
            self.bot.servers[server.id].settings[setting] = val
            self.bot.servers[server.id].saveSettingsState()
            await self.client.say("Setting `{}` added with value `{}`"
                            .format(setting, val))
            return

    @settings.command(pass_context=True, no_pm=True)
    async def list(self, ctx):
        server = ctx.message.server
        # TODO: Need to come up with a good way to display in table
        settingList = "\n".join(["`{}: {}`".format(x, y) for (x,y) in
                                 self.bot.servers[server.id].settings.items()])
        await self.client.say("Here is a list of settings:\n{}"
                              .format(settingList))
        return

    @settings.command(pass_context=True, no_pm=True)
    async def change(self, ctx, setting, newVal):
        server = ctx.message.server
        if setting not in self.bot.servers[server.id].settings:
            # This is not a setting yet
            await self.client.say("""This is not a valid setting. You can list the valid settings with `settings list`""")
            return
        else:
            # This is a setting we can change
            oldVal = self.bot.servers[server.id].settings[setting]
            self.bot.servers[server.id].settings[setting] = newVal
            self.bot.servers[server.id].saveSettingsState()
            await self.client.say("Setting `{}` changed from `{}` to `{}`."
                            .format(setting, oldVal, newVal))
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
            oldVal = self.bot.servers[server.id].settings[setting]
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
            self.bot.servers[server.id].reactions[name] = (regex, reply, probability)
            await self.client.say("Reaction `{}` added.")
            return

    @reactions.group(pass_context=True, no_pm=True, aliases=['change'])
    async def rchange(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument
            return

    @rchange.command(pass_context=True, no_pm=True)
    async def regex(self, ctx, name, newVal):
        await self.client.say("Accessed")
        return
    #     elif mode.lower() == "change":
    #         if not reaction or not regex or not reply:
    #             await self.client.say("Improper parameters.\n{}"
    #                             .format(self.reactionsUsage()))
    #             return
    #         if regex.lower() == "regex":
    #             return
    #         elif regex.lower() == "reply":
    #             return
    #         elif regex.lower() == "probability":
    #             return
    #         else:
    #             await self.client.say("Unrecognized key.\n{}"
    #                             .format(self.reactionsUsage()))
    #             return
    #         return
    #     elif mode.lower() == "remove":
    #         if not reaction:
    #             await self.client.say("Improper parameters.\n{}"
    #                             .format(self.reactionsUsage()))
    #             return
    #         # TODO: Creat a way to store reactions in the server object
    #         return
    #     else:
    #         await self.client.say("Unrecognized modification mode.\n{}"
    #                         .format(self.reactionsUsage()))
    #         return
    #     return
