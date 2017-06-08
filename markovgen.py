#!/usr/bin/env python

# Written by Levi Schuck: https://github.com/LeviSchuck

import random

class Markov(object):

        def __init__(self, open_file):
                self.cache = {}
                self.open_file = open_file
                self.lines = self.file_to_lines()
                self.line_size = len(self.lines)
                self.database()



        def file_to_lines(self):
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


