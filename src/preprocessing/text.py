import nltk
from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters, hrf_experiment_output_path
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
nltk.download('stopwords')

class TextProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict) -> None:
        super().__init__()

        default_keys = {'column_to_apply'}
        parameters = process_parameters(parameters, default_keys)
        self.column_to_apply = parameters.get('column_to_apply')
        self.items_to_replace = parameters.get('items_to_replace', {})
        self.parameters = parameters
        self.stop_words = set(stopwords.words('english'))
        self.text_processing_output_path = hrf_experiment_output_path().joinpath("preprocessing/text/")

    def pre_processing(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:

        items_to_replace = kwargs.get('items_to_replace', self.items_to_replace)
        if items_to_replace is None:
            items_to_replace = {}

        data = self.clean_data(data, self.column_to_apply, items_to_replace)

        text_tasks = {
            "tokenize_words": self.word_tokenizer,
            "remove_stop_words": self.remove_stop_words,
        }

        parameters_keys: list = list(self.parameters.keys())
        parameters_keys = list(filter(
            lambda x: x != "column_to_index" and x != "column_to_apply",
            parameters_keys
        ))

        result = data
        for key in parameters_keys:
            text_function_result = text_tasks[key](result, self.column_to_apply, "")
            result = text_function_result

        return result

    def clean_data(self, data: pd.DataFrame, column_to_apply: str, items_to_replace: dict) -> pd.DataFrame:

        if len(items_to_replace) == 0:
            return data #Nenhuma alteração será feita

        for key, value in items_to_replace.items():
            data[column_to_apply] = data[column_to_apply].apply(
                lambda x: x.replace(key, value)
            )
        return data

    def remove_stop_words(self, data: pd.DataFrame, column_to_apply: str, new_column: str = "") -> pd.DataFrame:
        filtered_sentence = []
        feature = data[column_to_apply]

        for word in feature:
            if word not in self.stop_words:
                filtered_sentence.append(word)

        if len(filtered_sentence) == 0:
            return pd.DataFrame()
        else:
            filtered_sentence = pd.Series(filtered_sentence)

        data = self._set_result_in_dataframe_column(data, filtered_sentence, column_to_apply, new_column)
        return data

    def word_tokenizer(self, data: pd.DataFrame, column_to_apply: str, new_column: str = "") -> pd.DataFrame:
        feature = data[column_to_apply]
        words_array = []
        for row in feature:
            tokenized_row = word_tokenize(row)
            words_array.append(tokenized_row)

        words_serie = pd.Series(words_array)
        data = self._set_result_in_dataframe_column(data, words_serie, column_to_apply, new_column)
        return data

    def sentence_tokenizer(self, data: pd.DataFrame, column_to_apply: str, new_column: str = "") -> pd.DataFrame:
        feature = data[column_to_apply]
        words_array = []
        for row in feature:
            tokenized_row = sent_tokenize(row)
            words_array.append(tokenized_row)

        words_serie = pd.Series(words_array)
        data = self._set_result_in_dataframe_column(data, words_serie, column_to_apply, new_column)
        return data

    def remove_duplicated_words(self, data: pd.DataFrame, column_to_apply: str, new_column: str = "") -> pd.DataFrame:
        feature = data[column_to_apply]
        words_without_duplicates = []
        new_column_values = []
        for row in feature:
            words_without_duplicates = set(row)  # Row == ['word1', 'word2]
            words_without_duplicates = list(words_without_duplicates)
            new_column_values.append(words_without_duplicates)

        new_column_values = pd.Series(new_column_values)
        data = self._set_result_in_dataframe_column(data, new_column_values, column_to_apply, new_column)
        return data

    def pos_tagging(self, data: pd.DataFrame, column_to_apply: str):
        column_to_apply = column_to_apply + "_tokenized"
        feature = data[column_to_apply]
        pos_tagging_result = nltk.pos_tag(feature.values)
        return pos_tagging_result

    def named_entity_recognition(self):
        pass

    def stemming(self, data: pd.DataFrame, column_to_apply: str, new_column: str = "") -> pd.DataFrame:
        pst = PorterStemmer()
        new_serie = []
        stemmed_words = []
        for row in data[column_to_apply]:
            for word in row:
                stemmed_words.append(pst.stem(word))
            new_serie.append(stemmed_words)

        new_serie = pd.Series(new_serie)
        data = self._set_result_in_dataframe_column(data, new_serie, column_to_apply, new_column)
        return data

    def lemmatization(self, data: pd.DataFrame, column_to_apply: str, new_column: str = "") -> pd.DataFrame:
        lemmatizer = WordNetLemmatizer()
        new_serie = []
        for row in data[column_to_apply]:
            new_words = []
            for word in row:
                new_words.append(lemmatizer.lemmatize(word))
            new_serie.append(new_words)

        new_serie = pd.Series(new_serie)

        data = self._set_result_in_dataframe_column(data, new_serie, column_to_apply, new_column)
        return data

    def frequency(self, data: pd.DataFrame, column_to_apply: str):
        feature = data[column_to_apply]
        freq_dist = FreqDist(feature.values)
        return freq_dist

    def _set_result_in_dataframe_column(self, data: pd.DataFrame,
                                        result: pd.Series,
                                        column_to_apply: str,
                                        new_column: str) -> pd.DataFrame:
        if new_column == "":
            data[column_to_apply] = result
        else:
            data[new_column] = result

        return data