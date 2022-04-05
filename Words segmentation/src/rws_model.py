from typing import List
from random import randint


class RWSModel:

    def __init__(self, border_temp: float, cooling_rate: float, iter_amount: int):

        self.border_temp = border_temp
        self.cooling_rate = cooling_rate
        self.iter_amount = iter_amount

    def flip(self, segments, position):
        return segments[:position] + str(1 - int(segments[position])) + segments[position + 1 :]

    def flip_n(self, segments, n):

        for _ in range(n):
            segments = self.flip(segments, randint(0, len(segments) - 1))

        return segments

    def segment(self, segments: str, sentence) -> List[str]:

        words: List[str] = []
        last: int = 0

        for index, segment in enumerate(segments):
            if segment == '1':
                words.append(sentence[last:index + 1])
                last = index + 1

        words.append(
            sentence[last:]
        )

        return words

    def evaluate(self, segments: str, sentence: str) -> int:

        words = self.segment(segments, sentence)
        score = sum(len(word) + 1 for word in set(words)) + len(words)

        return score

    def anneal(self, segments: str, sentence: str):

        collection = {}
        temperature = float(len(segments))

        while temperature > self.border_temp:
            best_segments, best_score = segments, self.evaluate(segments, sentence)

            for _ in range(self.iter_amount):
                guess = self.flip_n(segments, round(temperature))
                score = self.evaluate(guess, sentence)

                if score < best_score:
                    best_score, best_segments = score, guess

            score, segments = best_score, best_segments
            temperature /= self.cooling_rate
            collection[self.evaluate(segments, sentence)] = self.segment(segments, sentence)

            return collection


