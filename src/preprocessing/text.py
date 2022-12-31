import nltk
from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters, hrf_experiment_output_path
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from nltk import ne_chunk
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

nltk.download('punkt')


class TextProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        default_keys = {'apply_on'}
        super().__init__()
        parameters = process_parameters(parameters, default_keys)
        self.apply_on = parameters['apply_on']
        del parameters['apply_on']
        self.parameters = parameters
        self.stop_words = set(stopwords.words('english'))
        self.tfidf = TfidfVectorizer()
        self.text_processing_output_path = hrf_experiment_output_path().joinpath("preprocessing/text/")

    def pre_processing(self, data: pd.DataFrame, **kwargs):
        """

        @param data:
        @return:
        """

        data['genres'] = data['genres'].apply(
            lambda x: x.replace("|", " ")
        )

        text_tasks = {
            "tokenize_words": self.word_tokenizer,
            "remove_stop_words": self.remove_stop_words,
            "pos_tagging": self.pos_tagging,
            "tf_idf": self.tf_idf,
            "stemming": self.stemming,
            "lemmatization": self.lemmatization
        }

        parameters_keys = self.parameters.keys()
        print('parameters keys: ', parameters_keys)

        new_dataset = None
        result = data
        for key in parameters_keys:
            text_function_result = text_tasks[key](result)
            result = text_function_result

        print("Resultado final:", result)

    def remove_stop_words(self, data: pd.DataFrame, column_to_apply: str) -> pd.DataFrame:
        filtered_sentence = []
        feature = data[column_to_apply]

        for word in feature:
            if word not in self.stop_words:
                filtered_sentence.append(word)

        if len(filtered_sentence) == 0:
            return pd.DataFrame()
        else:
            filtered_sentence = pd.Series(filtered_sentence)

        data[column_to_apply] = filtered_sentence

        return data

    def word_tokenizer(self, data: pd.DataFrame, column_to_apply: str) -> pd.DataFrame:
        feature = data[column_to_apply]
        words_array = []
        for row in feature:
            tokenized_row = word_tokenize(row)
            words_array.append(tokenized_row)

        words_serie = pd.Series(words_array)
        name_new_feature = column_to_apply + "_word_tokens"
        data[name_new_feature] = words_serie
        return data

    def sentence_tokenizer(self, data: pd.DataFrame, column_to_apply: str) -> pd.DataFrame:
        feature = data[column_to_apply]
        words_array = []
        for row in feature:
            tokenized_row = sent_tokenize(row)
            words_array.append(tokenized_row)

        words_serie = pd.Series(words_array)
        name_new_feature = column_to_apply + "_sent_tokens"
        data[name_new_feature] = words_serie
        return data

    def remove_duplicated_words(self, data: pd.DataFrame, column_to_apply: str) -> pd.DataFrame:
        feature = data[column_to_apply]
        words_without_duplicates = []
        new_column_values = []
        for row in feature:
            words_without_duplicates = set(row)  # Row == ['word1', 'word2]
            words_without_duplicates = list(words_without_duplicates)
            new_column_values.append(words_without_duplicates)

        new_column_values = pd.Series(new_column_values)
        data['words_without_duplicates'] = new_column_values
        return data

    def pos_tagging(self, data: pd.DataFrame, column_to_apply: str):
        column_to_apply = column_to_apply + "_tokenized"
        feature = data[column_to_apply]
        pos_tagging_result = nltk.pos_tag(feature.values)
        return pos_tagging_result

    def named_entity_recognition(self):
        pass

    def tf_idf(self, data: pd.DataFrame, column_to_apply: str):
        column_to_indexing = "title"
        feature_to_indexing = data[column_to_indexing]
        feature = data[column_to_apply]
        feature_matrix = self.tfidf.fit_transform(data)

        similarity_matrix = linear_kernel(feature_matrix, feature_matrix)

        # Mapping pode ir para a parte do algoritmo
        mapping = pd.Series(data.index, index=feature_to_indexing)

        similarity_matrix.to_csv(self.text_processing_output_path)

    def stemming(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def lemmatization(self, data: pd.DataFrame) -> pd.DataFrame:

        lemmatizer = None

    def frequency(self, data: pd.DataFrame, column_to_apply: str):
        feature = data[column_to_apply]
        freq_dist = FreqDist(feature.values)
        return freq_dist
