import logging

from db.connection import get_db_connection


def create_definition(word_id, definition):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO definitions (word_id, definition) VALUES (%s, %s) RETURNING definition_id;",
                    (word_id, definition),
                )
                definition_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f'Added definition "{definition}" with id {definition_id}')
                return definition_id
    except Exception as e:
        logging.error(
            f"Error in create_definition query query for word_id {word_id}: {e}"
        )
    


def get_definition(word_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT definition FROM definitions WHERE word_id = %s;",
                    (word_id,),
                )
                definition = cur.fetchone()[0]
                logging.info(f'Got definition "{definition}" with word_id {word_id}')
                return definition
    except Exception as e:
        logging.error(f"Error in get_definition query for word_id {word_id}: {e}")
    


def get_definition_id(word_id, definition):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT definition_id FROM definitions WHERE definition = %s AND word_id = %s;",
                    (definition, word_id),
                )
                definition_id = cur.fetchone()
                logging.info(f"Got definition id for definition {definition}")
                return definition_id
    except Exception as e:
        logging.error(f"Error in get_definition_id query: {e}")
    
