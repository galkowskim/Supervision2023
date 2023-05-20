import pandas as pd
import re
from nltk.tokenize import word_tokenize
import spacy

class Preprocessor:
    def __init__(self, df: pd.DataFrame, stopwords_file: str) -> None:
        self.df
        with open('../data/stop_words_polish.txt', 'r', encoding='utf-8') as file:
            content = file.readlines()
            content = [line.strip() for line in content]
            self.stop_words = set(content)

    def preprocess_data(self, text_col: str):
        self.remove_special_characters(text_col)

    def remove_special_characters(self, text_col: str):
        """
        Removes special chcarcters from text column
        """
        special_chars = '[^A-Za-z0-9]+'
        self.df[text_col] = self.df[text_col].apply(lambda s: re.sub(special_chars, '', s))

    def _remove_stopwords_in_text(self, text: str):
            word_tokens = word_tokenize(text)
            filtered_sentence = [w for w in word_tokens if not w in self.stop_words]
            return ' '.join(filtered_sentence)

    def remove_stopwords(self, text_col: str):
        """
        Removes stopwords from polish language (provided we are scraping data from polish sites only)
        """
        self.df[text_col] = self.df[text_col].apply(lambda s: self._remove_stopwords_in_text(s))

    def _lemmatize_text(self, text):
        nlp = spacy.load("pl_core_news_sm")
        doc = nlp(text)
        return str([token.lemma_ for token in doc])

    def lemmatize(self, text_col):
        self.df[text_col] = self.df[text_col].apply(lambda s: self._lemmatize_text(s))

    def convert_text_to_lowercase(self, text_col: str):
        self.df[text_col] = self.df[text_col].str.lower()


