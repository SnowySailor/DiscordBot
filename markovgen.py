#!/usr/bin/env python

# Written by Levi Schuck: https://github.com/LeviSchuck
# Modified and added to by Nick Kanel: https://github.com/SnowySailor

import random
import os

class Markov(object):

        def __init__(self, open_file, max_size):
                self.cache = {}
                self.open_file = open_file
                self.lines = self.file_to_lines(max_size)
                self.line_size = len(self.lines)
                self.database()

        def file_to_lines(self, max_size):
            if os.stat(self.open_file.name).st_size > max_size: # If the file is greater than the max size in the config file..
                # We only want to get the last max_size bytes from it
                self.open_file.seek(-1 * max_size, os.SEEK_END)
            else:
                self.open_file.seek(0)
            data=self.open_file.read()
            lines = data.split('\n')
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
                        w1, w2 = w2, random.choice(self.cache[(w1, w2)])
                """gen_words.append(w3) """
                return ' '.join(gen_words)


        def digest_single_message(self, message):
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

