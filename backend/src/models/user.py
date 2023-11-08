import logging

from db.queries import create_user


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def create_user(self):
        try:
            user_id = create_user(self.username, self.email, self.password)
            return user_id
        except Exception as e:
            logging.error(
                f"Error in create_user method with user {self.username} {self.email}: {e}"
            )
            raise e
