import logging

from app.db.connection import get_db_connection


def create_user_review(user_id, word_id, review_date):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO user_reviews (user_id, word_id, review_date) VALUES (%s, %s, %s) RETURNING user_review_id;",
                    (
                        user_id,
                        word_id,
                        review_date,
                    ),
                )
                user_review_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f'Added user_review for word_id "{word_id}" with id {user_review_id}')
                return user_review_id
    except Exception as e:
        logging.error(f"Error in create_user_review query: {e}")
    finally:
        conn.close()
