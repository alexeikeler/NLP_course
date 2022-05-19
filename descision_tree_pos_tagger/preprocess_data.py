
class PPData:

    @staticmethod
    def features(sentence, index):

        return {
            'word': sentence[index],
            'is_first': index == 0,
            'is_last': index == len(sentence) - 1,
            'is_capitalized': sentence[index][0].upper() == sentence[index][0],
            'is_all_caps': sentence[index].upper() == sentence[index],
            'is_all_lower': sentence[index].lower() == sentence[index],
            'prefix-1': sentence[index][0],
            'prefix-2': sentence[index][:2],
            'prefix-3': sentence[index][:3],
            'suffix-1': sentence[index][-1],
            'suffix-2': sentence[index][-2:],
            'suffix-3': sentence[index][-3:],
            'prev_word': '' if index == 0 else sentence[index - 1],
            'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
            'has_hyphen': '-' in sentence[index],
            'is_numeric': sentence[index].isdigit(),
            'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
        }

    @staticmethod
    def untag(sent):
        return [w for w, _ in sent]

    @staticmethod
    def unword(sent):
        return [t for _, t in sent]

    @staticmethod
    def transform_to_dataset(tagged_sentences):

        x, y = [], []

        for tagged in tagged_sentences:
            for index, _ in enumerate(tagged):
                x.append(PPData.features(PPData.untag(tagged), index))
                y.append(tagged[index][1])

        return x, y

    @staticmethod
    def split(sent):

        words, tags = [], []
        _ = [(words.append(w), tags.append(t)) for w, t in sent]
        return words, tags
