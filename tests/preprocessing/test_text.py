import pytest
from src.data.movielens import MovieLens
from src.preprocessing.text import TextProcessing
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
import numpy as np
from nltk.corpus import stopwords

movies = MovieLens({
    'proportion': "ml-latest-small",
    'filters': {}
}).items

text_processing = TextProcessing({
    "apply_on": ["genres"],
    "remove_stop_words": True,
    "tokenize_words": True,
    "tokenize_sent": False,
    "tf_idf": True,
    "remove_caracters": False,
    "unicode_sentences": True,
    "pos_tagging": True,
    "column_to_index": "title"
})


class TestTextProcessing:

    def test_pre_processing(self):

        pass

    def test_pos_tagging(self):
        pass

    def test_lemmatization(self):
        pass

    def test_stemming(self):
        pass

    def test_word_tokenizer(self):
        movies['genres'] = movies['genres'].apply(
            lambda x: x.replace("|", " ")
        )

        new_data = text_processing.word_tokenizer(movies, 'genres')
        assert isinstance(new_data, pd.DataFrame) is True

        unexpected_values = []
        all_arrays_values = []
        for row in new_data['genres_word_tokens']:
            if isinstance(row, list):
                all_arrays_values.append(True)
            else:
                all_arrays_values.append(False)
                unexpected_values.append(row)

        assert np.all(all_arrays_values)

    def test_sent_tokenizer(self):

        pass

    def test_remove_duplicated_words(self):
        dataframe = pd.DataFrame(columns=['categories'])
        categories = pd.Series(['X', 'Y', 'Z', 'Y', 'Y', 'X', 'Z', 'Z'])
        dataframe['categories'] = categories

        result = text_processing.remove_duplicated_words(dataframe, 'categories')
        non_duplicated_values = result['categories'].values
        non_duplicated_values = set(non_duplicated_values)

        categories_set = set(categories.values)

    def test_remove_stop_words(self):
        stopwords_english = set(stopwords.words('english'))
        stopwords_english_values = pd.Series(list(stopwords_english))
        stop_df = pd.DataFrame(columns=['stop_words'])
        stop_df['stop_words'] = stopwords_english_values

        dataframe = text_processing.remove_stop_words(stop_df, 'stop_words')

        assert isinstance(dataframe, pd.DataFrame) is True
        assert dataframe.empty is True
