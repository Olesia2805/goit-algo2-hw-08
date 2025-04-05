import time
from typing import Dict
import random


class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        self.user_last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        last_message_time = self.user_last_message_time.get(user_id, 0.0)
        return (current_time - last_message_time) >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        if not self.can_send_message(user_id):
            return False
        self.user_last_message_time[user_id] = time.time()
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        last_message_time = self.user_last_message_time.get(user_id, 0.0)
        if self.can_send_message(user_id):
            return 0.0
        return max(0.0, self.min_interval - (current_time - last_message_time))


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Simulating the flow of messages (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}"
        )

        # Random delay between messages
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 4 seconds...")
    time.sleep(4)

    print("\n=== New series of messages after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}"
        )
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()
