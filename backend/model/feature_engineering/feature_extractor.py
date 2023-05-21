import pandas as pd
from typing import List, Dict


class FeatureExtractor:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

    def feature_engineering(self, text_col: str, terms_dict: Dict[str, List[str]], acc_creation_date_col, post_upload_date_col,  postprocessed=False):
        """
        Creates features on preprocessed data or pre and postprocessed data
        """
        if not postprocessed:
            self.count_number_of_exclamation_mark(text_col)
            self.count_number_of_uppercased_words(text_col)
            self.get_n_of_days_from_account_creation(
                acc_creation_date_col, post_upload_date_col, 'days_between_creation_and_post')
        else:
            for col_name, terms in terms_dict.items():
                self.extract_term_occurence(
                    text_col, terms=terms, new_col=col_name)
            self.get_text_length(text_col, 'text_length')

    def _terms_in_string(self, terms: List[str], text: str):
        """
        Returns 1 if all of the terms specified in list are present in the text.
        Helper function for extract_term_occurence function
        #TODO dodac count a nie 1/0
        """
        return 1 if all([term in text for term in terms]) else 0

    def count_word_occurrences(word_list, text):
        unique_words = set(word_list)
        common_words = unique_words.intersection(set(text.split()))
        total_count = sum(text.split().count(word) for word in common_words)
        return total_count

    def extract_term_occurence(self, text_col: str, terms: List[str], new_col: str):
        """
        Creates new column with name new_col based on the occurence of term(s) in text column
        """
        self.df[new_col] = self.df[text_col].apply(
            lambda s: self._terms_in_string(terms=terms, text=s))

    def count_number_of_uppercased_words(self, text_col: str, new_col: str = 'upper_words_count'):
        """
        Creates new column with name new_col based on the number of uppercased words in text column
        """
        self.df[new_col] = self.df[text_col].apply(
            lambda s: len([el for el in s.split(' ') if el.isupper()]))

    def count_number_of_exclamation_mark(self, text_col: str, new_col: str = "exclamation_marks_count"):
        """
        Creates new column with name new_col based on the number of exclamation marks in text column
        """
        self.df[new_col] = self.df[text_col].apply(lambda s: s.count("!"))

    def get_n_of_days_from_account_creation(self, acc_creation_date_col: str, post_upload_date_col: str, new_col: str):
        """
        Creates new column with name new_col based on the number of days between account creation and post upload
        """
        self.df[new_col] = (self.df[acc_creation_date_col] -
                            self.df[post_upload_date_col]).dt.components['hours']

    def get_text_length(self, text_col: str, new_col: str = 'text_length'):
        """
        Creates new column with name new_col based on the length of text column
        """
        self.df[new_col] = self.df[text_col].apply(lambda s: len(s))
