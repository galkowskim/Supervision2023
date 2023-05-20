import pandas as pd

class Preprocessor:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df

    def remove_special_characters(self, text_col: str):
        """
        Removes special chcarcters from text column
        """
        self.df[text_col] = self.df[text_col].str.replace('\n', '')