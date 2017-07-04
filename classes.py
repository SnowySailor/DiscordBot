import os
import pickle
from enum import Enum
from markovgen import Markov


class DiscordBot:
    def __init__(self, settings, botSettings, reactions=None):
        self.defaultServerSettings = settings
        self.defaultServerReactions = reactions
        self.botSettings = botSettings
        self.servers = dict()

    def addServer(self, server, settings=None, messages=0):
        if server.id in self.servers:
            return
        if not settings:
            settings = self.defaultServerSettings
        self.servers[server.id] = DiscordServer(server, settings, messages)


class DiscordServer:
    def __init__(self, server, settings, messages=0):
        self.markov = Markov(initEmpty=True)
        self.server = server

        # Check to see if we have serialized data stored for this server
        # `settings` and `reactions` hold individual settings for each server
        if not self.tryLoadSettingsState():
            self.settings = settings
        if not self.tryLoadReactionsState():
            self.reactions = dict()

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
                    if 'markovDigestLength' in self.settings['markov']:
                        lengthRestriction = self.settings['markov']['markovDigestLength']
                    elif 'markovSentenceLength' in settings['markov']:
                        lengthRestriction = self.settings['markov']['markovSentenceLength']
                    self.markov = Markov(f, self.settings['markov']['maxMarkovBytes'], False, lengthRestriction)
                    print("Loaded {} messages from file.".format(self.markov.line_size))

    def saveSettingsState(self):
        with open("data/{}_server_settings.pickle".format(self.server.id), "wb") as f:
            pickle.dump(self.settings, f)
        return

    def saveReactionsState(self):
        with open("data/{}_reactions.pickle".format(self.server.id), "wb") as f:
            pickle.dump(self.reactions, f)
        return

    def tryLoadSettingsState(self):
        if os.path.isfile("data/{}_server_settings.pickle".format(self.server.id)):
            with open("data/{}_server_settings.pickle".format(self.server.id), "rb") as f:
                # Load the data into the servers variable
                self.settings = pickle.load(f)
            return True
        return False

    def tryLoadReactionsState(self):
        if os.path.isfile("data/{}_reactions.pickle".format(self.server.id)):
            with open("data/{}_reactions.pickle".format(self.server.id), "rb") as f:
                # Load the data into the reactions variable
                self.reactions = pickle.load(f)
            return True
        return False


class TimeDenum(Enum):
    S = 1
    M = 2
    H = 3
