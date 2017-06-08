import os
from markovgen import Markov


class DiscordBot:
    def __init__(self, settings):
        self.markov = dict()  # Dict of {serverId: DiscordServer}
        self.settings = settings


class DiscordServer:
    def __init__(self, server, settings, messages=0):
        self.markovMessages = messages
        self.markov = None
        # If the log exists, we can check to see how many lines it has
        if os.path.isfile("logs/{}_chat_log".format(server.id)):
            i = 0
            with open("logs/{}_chat_log".format(server.id), "r",
                      encoding='utf-8', errors='ignore') as f:
                for i, l in enumerate(f):
                    pass
                # We can load the markov if there are greater than minMarkov messages
                if i+1 >= settings['minMarkov']:
                    self.markov = Markov(f, settings['maxMarkovBytes'])
            self.markovMessages = i + 1
