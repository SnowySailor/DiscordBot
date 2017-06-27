#!/usr/bin/env python

# Written by Levi Schuck: https://github.com/LeviSchuck
# Modified and added to by Nick Kanel: https://github.com/SnowySailor

import random

class Markov(object):

        def __init__(self, open_file=None, max_size=5000000, initEmpty=False, min_length=None):
                if initEmpty:
                    self.cache = {}
                    self.lines = []
                    self.line_size = 0
                else:
                    self.cache = {}
                    self.open_file = open_file
                    self.lines = self.file_to_lines(max_size, min_length)
                    self.line_size = len(self.lines)
                    self.database()

        def file_to_lines(self, max_size, min_length):
            self.open_file.seek(0)
            data = self.open_file.read()
            lines = []
            # Number of bytes that we have read in
            sizeRead = 0
            # Start at the end of the file so that we get the newest data
            for line in reversed(data.split('\n')):
                # Get the size of the current line
                lineSize = len(line.encode('utf-8'))
                # If this line would overshoot the limit, quit reading
                if sizeRead + lineSize > max_size:
                    break
                # If we have a min length set and the message is longer
                # then we can append it to the list and add to sizeRead
                if min_length and len(line.split()) >= min_length:
                    lines.append(line)
                    sizeRead += lineSize
                # If we don't have min length set, then we just read in
                # all the lines that are 3 words and longer.
                elif not min_length and len(line.split()) >= 3:
                    lines.append(line)
                    sizeRead += lineSize
            return lines

        def triples(self):
                """ Generates triples from the given data string. So if our string were
                                "What a lovely day", we'd generate (What, a, lovely) and then
                                (a, lovely, day).
                """
                """ Triples are too revealing.  Use doubles"""
                for line in self.lines:
                        line = line.split()
                        if len(line) < 3:
                                continue

                        for i in range(len(line) - 2):
                                yield (line[i], line[i+1], line[i+2])
                        yield(line[len(line) - 2], line[len(line) - 1], "\n")

        def database(self):
                for w1, w2, w3 in self.triples():
                        key = (w1, w2)
                        if key in self.cache:
                                self.cache[key].append(w3)
                        else:
                                self.cache[key] = [w3]

        def generate_markov_text(self, size=25):
                while True:
                    seed_line = self.lines[random.randint(0, self.line_size)].split()
                    if len(seed_line) > 2:
                        break
                seed_word, next_word = seed_line[0], seed_line[1]
                w1, w2 = seed_word, next_word
                gen_words = []
                for i in range(size):
                        if(w1 == "\n"):
                            break
                        gen_words.append(w1)
                        if(w2 == "\n"):
                            break
                        """ Get new words with more tollerance to letter case
                            Given a string like
                                "Hello there Tim and Bob"
                                Where w1 = "there"
                                      w2 = "Tim"
                                      (new word "and")
                            It could also select "it's" from a string like
                                "Look over there tim it's a seagull"
                            Because we also check to see if there are lower case versions
                            of the (w1,w2) pair in the cache.
                        """
                        #lowerKeyList = []
                        #if (w1.lower(),w2.lower()) in self.cache:
                        #    lowerKeyList = self.cache[(w1.lower(),w2.lower())]
                        #w1, w2 = w2, random.choice(list(set().union(self.cache[(w1, w2)], lowerKeyList)))
                        w1, w2 = w2, random.choice(self.cache[(w1, w2)])
                """gen_words.append(w3) """
                return ' '.join(gen_words)

        def digest_single_message(self, message):
            # Add the new message as a new line
            self.lines.append(message)
            # Increse the total number of lines we have
            self.line_size += 1

            for w1, w2, w3 in self.tipple_one_word(message):
                key = (w1, w2)
                if key in self.cache:
                    self.cache[key].append(w3)
                else:
                    self.cache[key] = [w3]

        def tipple_one_word(self, message):
            line = message.split()
            if len(line) < 3:
                return
            for i in range(len(line)-2):
                yield (line[i], line[i+1], line[i+2])
            yield(line[len(line) - 2], line[len(line) - 1], "\n")
