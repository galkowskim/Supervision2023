import pandas as pd
import re
from nltk.tokenize import word_tokenize
import spacy
spacy.load('pl_core_news_sm')


class Preprocessor:
    def __init__(self, df: pd.DataFrame, stopwords_file: str) -> None:
        self.df = df.copy()
        with open(stopwords_file, 'r', encoding='utf-8') as file:
            content = file.readlines()
            content = [line.strip() for line in content]
            self.stop_words = set(content)

    def preprocess_data(self, text_col: str, account_creation_date_col: str, post_upload_date_col: str):
        """
        Performs preprocessing tasks on text data
        """
        self.df = self.df[[text_col, account_creation_date_col, post_upload_date_col]]
        self.format_col_type(text_col, 'str')
        self.format_col_type(account_creation_date_col, 'datetime64[ns]')
        self.format_col_type(post_upload_date_col, 'datetime64[ns]')
        self.remove_special_characters(
            text_col, chars_to_delete='[^A-Za-zążźółćśęń!]+')
        self.remove_stopwords(text_col)

    def postprocess_data(self, text_col: str):
        """
        Performs postprocessing tasks on text data. These are the transformations, which would corrupt
        feature engineering process
        """
        self.remove_special_characters(
            text_col, chars_to_delete='[^A-Za-zążźółćśęń]+')
        self.convert_text_to_lowercase(text_col)
        self.lemmatize(text_col)
        self.remove_stopwords(text_col)

    def remove_special_characters(self, text_col: str, chars_to_delete: str):
        """
        Removes special chcarcters from text column
        """
        self.df[text_col] = self.df[text_col].str.replace('%', 'procent')
        self.df[text_col] = self.df[text_col].apply(
            lambda s: re.sub(chars_to_delete, ' ', s))

    def _remove_stopwords_in_text(self, text: str):
        word_tokens = word_tokenize(text)
        filtered_sentence = [
            w for w in word_tokens if not w in self.stop_words]
        return ' '.join(filtered_sentence)

    def remove_stopwords(self, text_col: str):
        """
        Removes stopwords from polish language (provided we are scraping data from polish sites only)
        """
        self.df[text_col] = self.df[text_col].apply(
            lambda s: self._remove_stopwords_in_text(s))

    def _lemmatize_text(self, text):
        nlp = spacy.load("pl_core_news_sm")
        doc = nlp(text)
        return str([token.lemma_ for token in doc])

    def lemmatize(self, text_col):
        """
        Applies lemmatization process to text column, i.e. extract semantically important information about the word from every word in string.
        """
        self.df[text_col] = self.df[text_col].apply(
            lambda s: self._lemmatize_text(s))

    def convert_text_to_lowercase(self, text_col: str):
        """
        Converts all words to lowercase type
        """

        self.df[text_col] = self.df[text_col].apply(lambda s: s.lower())

    def format_col_type(self, col: str, target_type: str):
        """
        Converts column to the desired type
        """
        self.df[col] = self.df[col].astype(target_type)
