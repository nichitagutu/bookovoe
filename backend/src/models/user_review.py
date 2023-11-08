import logging

from db.queries import update_user_review, get_latest_user_review


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
        self.ease_factor = 1.3
        self.interval = 0
        self.repetitions = 0
        self.review_quality = 0

    def calculate_sm2_factors(ease_factor, interval, repetitions, review_quality):
        if review_quality >= 3:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = round(interval * ease_factor)
            repetitions += 1
        else:
            repetitions = 0
            interval = 1

        ease_factor = ease_factor + (
            0.1 - (5 - review_quality) * (0.08 + (5 - review_quality) * 0.02)
        )
        ease_factor = max(ease_factor, 1.3)

        return ease_factor, interval, repetitions

    def update_review(self, review_quality):
        try:
            previous_interval = 0
            ease_factor, interval, repetitions = self.calculate_sm2_factors(
                self.ease_factor, self.interval, self.repetitions, review_quality
            )

            self.ease_factor = ease_factor
            self.interval = interval
            self.repetitions = repetitions

            latest_review = get_latest_user_review(self.user_id, self.word_id)

            if latest_review:
                previous_interval = latest_review["interval"]

            user_review_id = update_user_review(self, previous_interval)
            self.review_id = user_review_id

            logging.info(
                f"Updated user_review {self.review_id} for user {self.user_id}"
            )
            return user_review_id
        except Exception as e:
            logging.error(f"Failed to update review for user {self.user_id}: {e}")
            raise
