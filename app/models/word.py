import logging

from app.db.queries import create_word


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
