import nltk
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter
from typing import List


class TextAnalyser:

    @staticmethod
    def filter(text_: str) -> List[str]:
        
        noun: str = 'NN'
        sw: set = set(stopwords.words('english'))
        re_tok = nltk.RegexpTokenizer(r'\w+')

        punct_free = re_tok.tokenize(text_)
        filtered = [w for w in punct_free
                        if not w.lower() in sw]

        f_tagged = nltk.pos_tag(filtered)

        nouns_only = [wc[0] for wc in f_tagged
                        if wc[1] == noun]
        
        return nouns_only

    @staticmethod
    def count_freq(words: List[str], amount: int) -> pd.DataFrame:

        df: pd.DataFrame = pd.DataFrame(
            Counter(words).most_common(amount),
            columns=['Words', 'Count']
        )

        return df

