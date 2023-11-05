import logging

from app.db.connection import get_db_connection


def create_word(word):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO words (word) VALUES (%s) RETURNING word_id;",
                    (word,),
                )
                word_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f'Added word "{word}" with id {word_id}')
                return word_id
    except Exception as e:
        logging.error(f"Error in create_word query: {e}")
    finally:
        conn.close()
