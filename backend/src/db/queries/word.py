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


def get_all_words_ids() -> list:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT word_id FROM words;")
                words_ids = cur.fetchall()
                logging.info(f"Got all words ids")
                return words_ids
    except Exception as e:
        logging.error(f"Error in get_all_words_ids query: {e}")


def get_all_words_and_definitions():
    words_and_definitions = dict()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM words;")
                words = cur.fetchall()
                logging.info(f"Got all words")
                for id_and_word in words:
                    cur.execute(
                        "SELECT definition FROM definitions WHERE word_id = %s;",
                        (id_and_word[0],),
                    )

                    definitions = cur.fetchall()
                    words_and_definitions[id_and_word[1]] = definitions

                return words_and_definitions

    except Exception as e:
        logging.error(f"Error in get_all_words query: {e}")

def get_words_and_defs_for_given_ids(word_ids):
    words_and_definitions = dict()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                for word_id in word_ids:
                    cur.execute("SELECT word FROM words WHERE word_id = %s;", (word_id,))
                    word = cur.fetchone()[0]
                    cur.execute(
                        "SELECT definition FROM definitions WHERE word_id = %s;",
                        (word_id,),
                    )

                    definitions = cur.fetchall()
                    words_and_definitions[word] = definitions

                return words_and_definitions

    except Exception as e:
        logging.error(f"Error in get_words_and_defs_for_given_ids query: {e}")


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
