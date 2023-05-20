import pandas as pd
from typing import List

class FeatureExtractor:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def feature_engineering(self):
        pass

    def _terms_in_string(self, terms: List[str], text: str):
        return 1 if any([term in text for term in terms]) else 0

    def extract_term_occurence(self, text_col: str, terms: str or List[str], new_col: str):
        """
        Creates new column with name new_col based on the occurence of term(s) in text column
        """
        self.df[new_col] = self.df[text_col].apply(lambda s: self._terms_in_string(s))

    def count_upper_words_in_string(self, text:str):
        count = 0
        for word in text:
            if len(word) < 3:
                continue
            upper = 0
            for i in range(len(word)):
                if word[i].isupper():
                    upper += 1
            if upper > 3:
                count += 1
        return count 
    
    def count_upper_words(self, text_col: str):
        self.df['upper_count'] = self.df[text_col].apply(lambda c: self.count_upper_words_in_string(c))

    

    def word_is_in_text(self, word, text):
        if word in text:
            return True
        else:
            return False
        
    def count_word(self, word, text):
        count =  text.count(word)
        return count
    
    

        



        