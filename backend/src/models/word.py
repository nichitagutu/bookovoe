import logging

from db.queries import create_word, get_all_words, get_word_id
from text_processing import prepare_text
from wordnet_interface import get_synset_key_value_definitions
from wordnet_interface import fetch_synset_ids_for_lemmas
from file_handling import (
    read_file_content,
    get_lemmas_from_file,
    write_synset_definitions_to_file,
)
from models.definition import Definition


class Word:
    def __init__(self, word):
        self.word = word

    def create_word(self):
        try:
            word_id = create_word(self.word)
            logging.info(f'Added word "{self.word}" with id {word_id}')
            return word_id
        except Exception as e:
            logging.error(f'Error in create_word method with word "{self.word}": {e}')
            raise e

    def get_word_id(self):
        try:
            word_id = get_word_id(self.word)
            if word_id:
                return word_id

            return None
        except Exception as e:
            logging.error(f'Error in does_exist method with word "{self.word}": {e}')
            raise e

    @staticmethod
    def get_all_words():
        try:
            words = get_all_words()
            logging.info(f"Got all words")
            return words
        except Exception as e:
            logging.error(f"Error in get_all_words method: {e}")
            raise e

    @staticmethod
    def save_words_from_text(cube, wordnet, text):
        words_from_file = prepare_text(text)
        lemmas = get_lemmas_from_file(cube, words_from_file)
        print("lemmas: ", lemmas)
        synset_ids = fetch_synset_ids_for_lemmas(wordnet, lemmas)
        definitions = get_synset_key_value_definitions(wordnet, synset_ids)
        for key, value in definitions.items():
            word = Word(key)
            word_id = word.get_word_id()
            if not word_id:
                word_id = word.create_word()

            for definition in value:
                definition = Definition(word_id, definition)
                definition_id = definition.get_definition_id()
                if not definition_id:
                    definition_id = definition.create_definition()

        return definitions
