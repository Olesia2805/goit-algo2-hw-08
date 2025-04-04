import random
from typing import Dict
import time
from collections import deque


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_messages: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str) -> None:
        current_time = time.time()
        if user_id in self.user_messages:
            while (
                self.user_messages[user_id]
                and self.user_messages[user_id][0] < current_time - self.window_size
            ):
                self.user_messages[user_id].popleft()

    def can_send_message(self, user_id: str) -> bool:
        return len(self.user_messages.get(user_id, deque())) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        if not self.can_send_message(user_id):
            return False
        if user_id not in self.user_messages:
            self.user_messages[user_id] = deque()
        self.user_messages[user_id].append(time.time())
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        self._cleanup_window(user_id)
        if self.can_send_message(user_id):
            return 0.0
        return max(
            0.0, (self.user_messages[user_id][0] + self.window_size) - time.time()
        )


# Demonstration of work
def test_rate_limiter():
    # Create rate limiter: window 10 seconds, 1 message
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Simulate the flow of messages from users (sequential IDs from 1 to 20)
    print("\n=== Simulating the flow of messages ===")
    for message_id in range(1, 11):
        # Simulate different users (ID from 1 to 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}"
        )

        # Small delay between messages for realism
        # Random delay from 0.1 to 1 second
        time.sleep(random.uniform(0.1, 1.0))

    # Wait for the window to clear
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
        # Random delay from 0.1 to 1 second
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
