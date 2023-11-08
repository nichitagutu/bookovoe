import logging

from psycopg2 import DatabaseError

from db.connection import get_db_connection


def update_user_review(
    user_review,
    previous_interval,
):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_word_reviews (user_id, word_id, review_date, ease_factor, interval, repetitions, review_quality, previous_interval)
                    VALUES (%s, %s, CURRENT_DATE + INTERVAL %s day, %s, %s, %s, %s)
                    RETURNING review_id;
                    """,
                    (
                        user_review.user_id,
                        user_review.word_id,
                        user_review.interval,
                        user_review.ease_factor,
                        user_review.interval,
                        user_review.repetitions,
                        user_review.review_quality,
                        previous_interval,
                    ),
                )
                review_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f"Updated user_word_review with id {review_id}")
                return review_id
    except DatabaseError as e:
        logging.error(f"Database error in update_user_review: {e}")
        raise
    except Exception as e:
        logging.error(f"Error in update_user_review: {e}")
        raise
    


def get_latest_user_review(user_id, word_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT review_id, ease_factor, interval, repetitions, review_quality, review_date
                    FROM user_word_reviews
                    WHERE user_id = %s AND word_id = %s
                    ORDER BY review_date DESC
                    LIMIT 1;
                    """,
                    (user_id, word_id),
                )
                review = cur.fetchone()
                logging.info(f"Got user_review for word_id {word_id}")
                return review
    except DatabaseError as e:
        logging.error(f"Database error in get_user_review: {e}")
        raise
    except Exception as e:
        logging.error(f"Error in get_user_review: {e}")
        raise
    
