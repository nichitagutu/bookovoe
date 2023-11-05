import logging

from app.db.queries import create_user_review


class UserReview:
    def __init__(
        self,
        user_id,
        word_id,
        review_date,
    ):
        self.user_id = user_id
        self.word_id = word_id
        self.review_date = review_date

    def create_user_review(self):
        try:
            user_review_id = create_user_review(
                self.user_id, self.word_id, self.review_date
            )
            logging.info(f'Added user_review "{self.review}" with id {user_review_id}')
            return user_review_id
        except Exception as e:
            logging.error(
                f'Error in create_user_review method for word_id "{self.word_id}" for user_id {self.user_id}: {e}'
            )
            raise e
