import logging
from datetime import datetime

from db.queries import (
    create_word,
    get_all_words_and_definitions,
    get_word_id,
    get_words_and_defs_for_given_ids,
)
from text_processing import prepare_text
from wordnet_interface import get_synset_key_value_definitions
from wordnet_interface import fetch_synset_ids_for_lemmas
from file_handling import get_lemmas_from_file
from models.definition import Definition
from models.user_review import UserReview


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
    def get_cards_to_learn(user_id, size):
        try:
            all_word_reviews = UserReview.get_all_word_reviews(user_id)
            current_time = datetime.now()

            words_to_review = set()
            overdue_reviews = set()
            upcoming_reviews = set()

            for word_id, review_date, interval, definition_id in all_word_reviews:
                if review_date is None:
                    words_to_review.add(word_id)
                elif review_date + interval < current_time:
                    overdue_reviews.add(word_id)
                else:
                    upcoming_reviews.add(word_id)

            words_to_learn = list(words_to_review) + list(overdue_reviews)

            if len(words_to_learn) < size:
                words_to_learn.extend(
                    list(upcoming_reviews)[: size - len(words_to_learn)]
                )

            words_and_defs = get_words_and_defs_for_given_ids(words_to_learn[:size])
            logging.info("Got all cards to learn")

            return words_and_defs
        except Exception as e:
            logging.error(f"Error in get_cards_to_learn method: {e}")
            raise e

    @staticmethod
    def get_all_words_and_definitions():
        try:
            words_and_definitions = get_all_words_and_definitions()
            logging.info(f"Got all words and their definitions")
            return words_and_definitions
        except Exception as e:
            logging.error(f"Error in get_all_words method: {e}")
            raise e

    @staticmethod
    def save_words_from_text(cube, wordnet, text):
        words_from_file = prepare_text(text)
        lemmas = get_lemmas_from_file(cube, words_from_file)
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
