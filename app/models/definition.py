import logging

from app.db.queries import create_definition


class Definition:
    def __init__(self, word_id, definition):
        self.word_id = word_id
        self.definition = definition

    def create_definition(self):
        try:
            definition_id = create_definition(self.word_id, self.definition)
            logging.info(
                f'Added definition "{self.definition}" with id {definition_id}'
            )
            return definition_id
        except Exception as e:
            logging.error(
                f'Error in create_definition method with definition "{self.definition}": {e}'
            )
            raise e
