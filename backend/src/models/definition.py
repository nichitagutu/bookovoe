import logging

from db.queries import create_definition, get_definition, get_definition_id


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
        
    def get_definition_id(self):
        try:
            definition_id = get_definition_id(self.word_id, self.definition)
            if definition_id:
                return definition_id
            
            return None
        except Exception as e:
            logging.error(
                f'Error in does_exist method with definition "{self.definition}": {e}'
            )
            raise e

    @staticmethod
    def get_definition(word_id):
        try:
            definition = get_definition(word_id)
            logging.info(f'Got definition "{definition}" with id {word_id}')
            return definition
        except Exception as e:
            logging.error(f"Error in get_definition method with id {word_id}: {e}")
            raise e
