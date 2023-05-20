import pandas as pd
from typing import List, Dict

class FeatureExtractor:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def feature_engineering(self, text_col: str, terms_dict: Dict[List[str]], postprocessed = False):
        """
        Creates features on preprocessed data or pre and postprocessed data
        """
        if not postprocessed:
            self.count_number_of_exclamation_mark()
            self.count_number_of_uppercased_words()
        else:
            for col_name, terms in terms_dict.items():
                self.extract_term_occurence(text_col, terms=terms, new_col=col_name)

    def _terms_in_string(self, terms: List[str], text: str):
        """
        Returns 1 if all of the terms specified in list are present in the text.
        Helper function for extract_term_occurence function
        """
        return 1 if all([term in text for term in terms]) else 0

    def extract_term_occurence(self, text_col: str, terms: List[str], new_col: str):
        """
        Creates new column with name new_col based on the occurence of term(s) in text column
        """
        self.df[new_col] = self.df[text_col].apply(lambda s: self._terms_in_string(terms=terms, text=s))
    
    def count_number_of_uppercased_words(self, text_col: str, new_col: str = 'upper_words_count'):
        self.df[new_col] = self.df[text_col].apply(lambda s: len([el for el in s.split(' ') if el.isupper()]))
    
    def count_number_of_exclamation_mark(self, text_col: str, new_col: str = "exclamation_marks_count"):
        self.df[new_col] = self.df[text_col].apply(lambda s: s.count("!"))
    
    def get_n_of_days_from_account_creation(self, acc_creation_date_col: str, post_upload_date_col: str):
        return self.df[acc_creation_date_col] - self.df[post_upload_date_col]
    
    

        



