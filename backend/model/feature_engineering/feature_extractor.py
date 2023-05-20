import pandas as pd

class FeatureExtractor:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def feature_engineering(self):
        pass

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
    
    def count_upper_words(self, text_col:str):

        self.df[upper_count] = self.df[text_col].apply(lambda c: self.count_upper_words_in_string(c))




    
    def word_is_in_text(self, word, text):
        if word in text:
            return True
        else:
            return False
        
    def count_word(self, word, text):
        count =  text.count(word)
        return count
    
    

        



        