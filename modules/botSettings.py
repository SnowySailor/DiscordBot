from discord.ext import commands


class SettingsCommands:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def modifySetting(self, ctx, mode=None, setting=None, newVal=None):
        """Allows changing of server settings"""
        def modifyUsage():
            return ("""Usage: `modifySetting change SETTING NEWVAL`\n
                    `modifySetting list` to list settings\n
                    `modifySetting add SETTING VAL`\n
                    `modifySetting remove SETTING`\n""")
        server = ctx.message.server

        # Permissions check
        # TODO: Allow admins to specify roles that can change bot settings
        # MAYBE TODO: If role is updated, give server admin a warning
        if not ctx.message.author.manage_server:
            self.client.say("""You are not a server manager and cannot
                             change my settings.""")
            return
        # Make sure the server exists in our bot
        if server.id not in self.bot.servers:
            self.bot.addServer(server, self.bot.defaultServerSettings)

        if mode.lower() == "list":
            # TODO: Need to come up with a good way to display in table
            settingList = "\n".join(["`{}`".format(x) for x in
                                     self.bot.servers[server.id].keys()])
            self.client.say("Here is a list of settings:\n{}"
                            .format(settingList))
            return

        # TODO: Fix because remove won't ever be able to trigger
        if not setting or not newVal:
            self.client.say(modifyUsage())
            return

        if mode.lower() == "add":
            if setting in self.bot.server[server.id].settings:
                # Setting is already in use
                self.client.say("""That is already a setting. You can modify
                                 it or remove it:\n{}""".format(modifyUsage()))
                return
            else:
                # This is a new setting
                self.bot.servers[server.id].settings[setting] = newVal
                self.bot.servers[server.id].saveSettingsState()
                self.client.say("Setting `{}` added with value `{}`"
                                .format(setting, newVal))
                return
        elif mode.lower() == "change":
            if setting not in self.bot.servers[server.id].settings:
                # This is not a setting yet
                self.client.say("""This is not a valid setting. You can list
                 the valid settings with `modifySetting list`""")
                return
            else:
                # This is a setting we can change
                oldVal = self.bot.servers[server.id].settings[setting]
                self.bot.servers[server.id].settings[setting] = newVal
                self.bot.servers[server.id].settings.saveSettingsState()
                self.client.say("Setting `{}` changed from `{}` to `{}`."
                                .format(setting, oldVal, newVal))
                return
        elif mode.lower() == "remove":
            if setting not in self.bot.servers[server.id].settings:
                # Can't delete a setting we don't have
                self.client.say("""This is not a valid setting. You can list the
                 valid settings with `modifySetting list`""")
                return
            else:
                # Delete the setting
                oldVal = self.bot.servers[server.id].settings[setting]
                del self.bot.servers[server.id].settings[setting]
                self.bot.servers[server.id].saveSettingsState()
                self.client.say("Setting `{}` removed.")
                return
        else:
            self.client.say("Unrecognized modification mode.\n{}"
                            .format(modifyUsage()))
            return
        return

    # TODO: Write
    @commands.command(pass_context=True, no_pm=True)
    async def modifyReaction(self, ctx, mode=None, reaction=None, regex=None,
                             reply=None, probability=None):
        def modifyReactionUsage():
            return ("""Usage: `modifyReaction change NAME
                     [regex|reply|probability] NEWVALUE`\n
                    `modifyReaction list` to list settings\n
                    `modifyReaction add NAME REGEX REPLY PROBABILITY`\n
                    `modifyReaction remove NAME`\n""")

        # Permissions check
        # TODO: Allow admins to specify roles that can change bot settings
        # MAYBE TODO: If role is updated, give server admin a warning
        if not ctx.message.author.manage_server:
            self.client.say("""You are not a server manager and cannot change
                            my settings.""")
            return

        if mode.lower() == "list":
            # TODO: Need to come up with a good way to display in table
            return
        elif mode.lower() == "add":
            if not reaction or not regex or not reply or not probability:
                self.client.say("Improper parameters.\n{}"
                                .format(modifyReactionUsage()))
                return
            #if regex.lower()
            return
        elif mode.lower() == "change":
            if not reaction or not regex or not reply:
                self.client.say("Improper parameters.\n{}"
                                .format(modifyReactionUsage()))
                return
            if regex.lower() == "regex":
                return
            elif regex.lower() == "reply":
                return
            elif regex.lower() == "probability":
                return
            else:
                self.client.say("Unrecognized key.\n{}"
                                .format(modifyReactionUsage()))
                return
            return
        elif mode.lower() == "remove":
            if not reaction:
                self.client.say("Improper parameters.\n{}"
                                .format(modifyReactionUsage()))
                return
            # TODO: Creat a way to store reactions in the server object
            return
        else:
            self.client.say("Unrecognized modification mode.\n{}"
                            .format(modifyReactionUsage()))
            return
        return
