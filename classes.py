import os
from markovgen import Markov


class DiscordBot:
    def __init__(self, settings):
        self.markov = dict()  # Dict of {serverId: DiscordServer}
        self.settings = settings


class DiscordServer:
    def __init__(self, server, settings, messages=0):
        #self.markovMessages = messages
        self.markov = Markov(initEmpty=True)
        self.markov.line_size = messages

        # If the log exists, we can check to see how many lines it has
        if os.path.isfile("logs/{}_chat_log".format(server.id)):
            i = 0
            with open("logs/{}_chat_log".format(server.id), "r",
                      encoding='utf-8', errors='ignore') as f:
                for i, l in enumerate(f):
                    pass
                # We can load the markov if there are messages in the file
                if i > 1:
                    print("Loaded data from file")
                    self.markov = Markov(f, settings['maxMarkovBytes'])
            self.markov.line_size = i + 1
