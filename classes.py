import redis
import os
import yaml
from enum import Enum
from markovgen import Markov
from string import Formatter
from collections import Mapping
from settingsMerger import mergeDicts
try:
    from _string import formatter_field_name_split
except ImportError:
    formatter_field_name_split = lambda \
        x: x._formatter_field_name_split()

class DiscordBot:
    def __init__(self, settings, botSettings, reactions=None):
        self.defaultServerSettings = settings
        self.defaultServerReactions = reactions
        self.botSettings = botSettings
        self.servers = dict()
        # # Only create a redis instance if we need it
        # if ('redisLimit' in self.botSettings and 
        #         self.botSettings['redisLimit']):
        self.redis = redis.StrictRedis(decode_responses=True)

    def addServer(self, server, settings=None, reactions=None, messages=0):
        if server.id in self.servers:
            return
        if not settings:
            settings = self.defaultServerSettings
        if not reactions:
            reactions = self.defaultServerReactions
        self.servers[server.id] = DiscordServer(server, settings, reactions, messages)


class DiscordServer:
    def __init__(self, server, defaultSettings, defaultReactions, messages=0):
        self.markov = Markov(initEmpty=True)
        self.server = server

        # Check to see if we have serialized data stored for this server
        # `settings` and `reactions` hold individual settings for each server
        if not self.readFromYamlData("settings", defaultSettings):
            self.settings = defaultSettings
        if not self.readFromYamlData("reactions"):
            self.reactions = defaultReactions
        if not self.readFromYamlData("whitelistChannels"):
            self.whitelistChannels = set()
        if not self.readFromYamlData("whitelistRoles"):
            self.whitelistRoles = set()
        if not self.readFromYamlData("channelOverwrites"):
            # Permissions overwrites
            # dict = {channel.id: set()}
            self.channelOverwrites = dict()

        # If the log exists, we can check to see how many lines it has
        if os.path.isfile("logs/{}_chat_log".format(server.id)):
            i = 0
            with open("logs/{}_chat_log".format(server.id), "r",
                      encoding='utf-8', errors='ignore') as f:
                for i, l in enumerate(f):
                    if i > 1:
                        break
                # We can load the markov if there are messages in the file
                if i > 1:
                    lengthRestriction = None
                    if 'digestLength' in self.settings['markov']:
                        lengthRestriction = self.settings['markov']['digestLength'][0]
                    elif 'sentenceLength' in settings['markov']:
                        lengthRestriction = self.settings['markov']['sentenceLength'][0]
                    self.markov = Markov(f, self.settings['markov']['maxBytes'][0], False, lengthRestriction)
                    print("Loaded {} messages from file.".format(self.markov.line_size))

    def dumpToYamlData(self, thing):
        # Made sure that there is actually the attribute
        if hasattr(self, thing):
            # Get the attribute
            attr = getattr(self, thing)
            # Dump it to the correct yaml file
            with open("data/{}_{}.yaml".format(self.server.id, thing), "w") as f:
                yaml.dump(attr, f)
                return True
        else:
            raise AttributeError("Object has no attr {}".format(thing))
        return

    def readFromYamlData(self, thing, default=None):
        if os.path.isfile("data/{}_{}.yaml".format(self.server.id, thing)):
            with open("data/{}_{}.yaml".format(self.server.id, thing), "r") as f:
                readData = yaml.load(f)
                if default is not None:
                    changes = mergeDicts(default, readData)
                setattr(self, thing, readData)
                return True
        return False

class TimeDenum(Enum):
    S = 1
    M = 2
    H = 3


# Classes for safely allowing users to use custom format strings in bot replies.
class AccessData:
    def __init__(self, author, clientUser):
        self.author = author
        self.clientUser = clientUser

class MagicFormatMapping(Mapping):
    """This class implements a dummy wrapper to fix a bug in the Python
    standard library for string formatting.

    See http://bugs.python.org/issue13598 for information about why
    this is necessary.
    """

    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self._last_index = 0

    def __getitem__(self, key):
        if key == '':
            idx = self._last_index
            self._last_index += 1
            try:
                return self._args[idx]
            except LookupError:
                pass
            key = str(idx)
        return self._kwargs[key]

    def __iter__(self):
        return iter(self._kwargs)

    def __len__(self):
        return len(self._kwargs)

class SafeFormatter(Formatter):
    def get_field(self, field_name, args, kwargs):
        first, rest = formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)
        for is_attr, i in rest:
            if is_attr:
                obj = self.safe_getattr(obj, i)
            else:
                obj = obj[i]
        return obj, first

    def safe_getattr(self, obj, attr):
        # Expand the logic here.  For instance on 2.x you will also need
        # to disallow func_globals, on 3.x you will also need to hide
        # things like cr_frame and others.  So ideally have a list of
        # objects that are entirely unsafe to access.
        if attr[:1] == '_':
            raise AttributeError(attr)
        return getattr(obj, attr)