import logging

from db.connection import get_db_connection


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
    


def get_all_words():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM words;")
                words = cur.fetchall()
                logging.info(f"Got all words")
                return words
    except Exception as e:
        logging.error(f"Error in get_all_words query: {e}")
    


def get_word_id(word):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT word_id FROM words WHERE word = %s;", (word,))
                word_id = cur.fetchone()
                logging.info(f"Got word id for word {word}")
                return word_id
    except Exception as e:
        logging.error(f"Error in get_word_id query: {e}")
    
