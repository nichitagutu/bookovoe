from app.db.connection import get_db_connection


def create_user(username, email, password):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id;",
                    (username, email, password),
                )
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id
    except Exception as e:
        print(f"Error in create_user query: {e}")
    finally:
        conn.close()
