import logging

from app.db.connection import get_db_connection


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
        logging.error(f"Error in create_definition query: {e}")
    finally:
        conn.close()
