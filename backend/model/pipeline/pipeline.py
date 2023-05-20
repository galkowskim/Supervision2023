import sys
sys.path.append('..')
from model.feature_engineering.feature_extractor import FeatureExtractor
import importlib
import pandas as pd
from model.preprocessing.preprocessor import Preprocessor

fe_dict = {'sprzedac': ['sprzedać'],
           'kupic': ['kupić'],
           'konto': ['konto'],
           'bankowy': ['bankowy'],
           'bankowosc': ['bankowość'],
           'zalozenie_konta': ['zapłaca', 'założeć'],
           'komornik': ['komornik'],
           'udostepnia': ['udostępnia'],
           'finanse': ['finanse'],
           'ryzyko': ['ryzyko'],
           'bezpieczny': ['bezpieczny'],
           'przelew': ['przelew'],
           'procent': ['procent'],
           'kwota': ['kwota'],
           'krypto': ['krypto'],
           'kryptowaluta': ['kryptowaluta'],
           'slupa': ['słupa'],
           'slup': ['słup'],
           'tylko': ['tylko'],
           'szybko': ['szybko'],
           'zysk': ['zysk'],
           'przelew': ['przelew'],
           'dane': ['dane'],
           'rozny_bank': ['różny', 'bank'],
           'prowizja': ['prowizja'],
           'otworzyc': ['otworzyć'],
           'zajecie_komornicze': ['zajęć', 'komornicz'],
           'oferta_ograniczona': ['oferta', 'ograniczyć'],
           'zakladane_w_oddziale': ['zakładać', 'oddział'],
           'brak_blokad': ['brak', 'blokad'],
           'brak_limitu': ['limit'],
           'dokumenty_bankowe': ['dokument', 'bank'],
           'umowa': ['umowa'],
           'karta': 'karta',
           'sim': ['sim'],
           'kaucja': ['kaucja'],
           'opłata': ['opłata'],
           'skan_dowodu': ['skan', 'dowód'],
           'dluga_wspolpraca': ['długi', 'współpraca'],
           'zbudowac_zaufanie': ['zbudować', 'zaufanie'],
           'gwarancja': ['gwarancja'],
           'legalny': ['legalny'],
           'pożyczka': ['pożyczka'],
           'powazna_propozycja': ['poważny', 'propozycja'],
           'dziś': ['dziś'],
           'teraz': ['teraz']}


class Pipeline:
    def __init__(self) -> None:
        pass

    @staticmethod
    def run(df, stopwords_file_path: str):
        preprocessor = Preprocessor(df, stopwords_file_path) #'../../../data/stop_words_polish.txt'
        preprocessor.preprocess_data(
            'desc', 'user_registration_date', 'post_creation', 'fake')
        df_preprocessed = preprocessor.df

        fe = FeatureExtractor(df_preprocessed)
        fe.feature_engineering(
            'desc', fe_dict, 'user_registration_date', 'post_creation')

        postprocessor = Preprocessor(
            fe.df, '../../../data/stop_words_polish.txt')
        postprocessor.postprocess_data('desc')
        df_preprocessed = postprocessor.df

        fe = FeatureExtractor(df_preprocessed)
        fe.feature_engineering(
            'desc', fe_dict, 'user_registration_date', 'post_creation', postprocessed=True)
        return fe.df
