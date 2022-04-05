import functools
import math


class PWSModel:

    def __init__(self):
        self.single_word_prob = FreqDist()

    @staticmethod
    def __split_pairs(word):
        return [(word[:index + 1], word[index+1:]) for index, _ in enumerate(word)]

    @staticmethod
    def memoize(f):
        cache = {}

        def memoized_func(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]

        memoized_func.cache = cache

        return memoized_func

    def __word_fitness(self, words):
        return functools.reduce(
            lambda x, y: x + y,
            (math.log10(self.single_word_prob(w)) for w in words)
        )

    @memoize
    def segment(self, word):
        if not word:
            return []
        word = word.lower()

        possible_segmentations = [
            [first] + self.segment(rest)
            for (first, rest) in self.__split_pairs(word)
        ]

        return max(possible_segmentations, key=self.__word_fitness)


class FreqDist(dict):

    def __init__(self):
        self.gram_count = 0
        self.path = 'data/one-grams.txt'
        self.count_freq()

    def __call__(self, word):
        if word in self:
            return float(self[word]) / self.gram_count
        else:
            # return 1 / self.gram_count
            return 1.0 / (self.gram_count * 10 ** len(word) - 2)

    def count_freq(self):

        for line in  open(self.path):
            (word, count) =line[:-1].split('\t')
            self[word] = int(count)
            self.gram_count += self[word]



