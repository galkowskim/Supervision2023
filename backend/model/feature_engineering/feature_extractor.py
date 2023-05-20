import pandas as pd
from typing import List

class FeatureExtractor:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def feature_engineering(self, text_col: str, postprocessed = False):
        """
        Creates features on preprocessed data or pre and postprocessed data
        """
        if not postprocessed:
            self.count_number_of_exclamation_mark()
            self.count_number_of_uppercased_words()
        else:
            for terms in term_list:
                self.extract_term_occurence(text_col, terms, )

    def _terms_in_string(self, terms: List[str], text: str):
        """
        Returns 1 if all of the terms specified in list are present in the text.
        Helper function for extract_term_occurence function
        """
        return 1 if all([term in text for term in terms]) else 0

    def extract_term_occurence(self, text_col: str, terms: str or List[str], new_col: str):
        """
        Creates new column with name new_col based on the occurence of term(s) in text column
        """
        self.df[new_col] = self.df[text_col].apply(lambda s: self._terms_in_string(terms=terms, text=s))
    
    def count_number_of_uppercased_words(self, text_col: str, new_col: str = 'upper_words_count'):
        self.df[new_col] = self.df[text_col].apply(lambda s: len([el for el in s.split(' ') if el.isupper()]))
    
    def count_number_of_exclamation_mark(self, text_col: str, new_col: str = "exclamation_marks_count"):
        self.df[new_col] = self.df[text_col].apply(lambda s: s.count("!"))
    
    

        



