from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from nltk import ne_chunk

"""
Possíveis processos para aplicar em cima do texto:

1. Remoção de stop-words
2. Tokenização
3. Stemming
4. Lemmatization
5. Remoção de caracteres indesejados
6. Remoção de acentos
7. Remoção de valores não alfanuméricos
8. Remoção de valores duplicados
9. TF-IDF
10. Pos tagging
11. Frequẽncia das palavras no documento
12. Named Entity Reconignition
"""

class TextProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        default_keys = set()
        super().__init__()
        parameters = process_parameters(parameters, default_keys)

    def pre_processing(self, data, **kwargs):
        """

        @param data:
        @return:
        """
        pass

    def remove_stop_words(self):
        pass
    def word_tokenizer(self):
        pass
    def sentence_tokenizer(self):
        pass

    def remove_duplicated_words(self):
        pass

    def pos_tagging(self):
        pass
    def named_entity_recognition(self):
        pass

    def tf_idf(self):
        pass

    def stemming(self):
        pass

    def lemmatization(self):
        pass

    def frequency(self):
        pass
