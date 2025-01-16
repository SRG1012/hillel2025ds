from abc import ABC, abstractmethod
from time import time

# Абстрактний клас для соціальних каналів
class SocialChannel(ABC):
    def __init__(self, followers: int):
        self.followers = followers

    @abstractmethod
    def post_message(self, message: str) -> None:
        pass

# Реалізація каналу YouTube
class YouTubeChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        print(f"Posting to YouTube: {message}")

# Реалізація каналу Facebook
class FacebookChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        print(f"Posting to Facebook: {message}")

# Реалізація каналу Twitter
class TwitterChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        print(f"Posting to Twitter: {message}")

# Клас для постів
class Post:
    def __init__(self, message: str, timestamp: int):
        self.message = message
        self.timestamp = timestamp

# функція для публікації повідомлення
def post_a_message(channel: SocialChannel, message: str) -> None:
    channel.post_message(message)

# Функція для обробки розкладу
def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        if post.timestamp <= time():
            for channel in channels:
                post_a_message(channel, post.message)

# Приклад використання
if __name__ == "__main__":
    youtube = YouTubeChannel(followers=1000)
    facebook = FacebookChannel(followers=2000)
    twitter = TwitterChannel(followers=1500)

    # Створюємо пости
    posts = [
        Post("Hello, world!", timestamp=int(time()) - 10),
        Post("New video coming soon!", timestamp=int(time()) + 60),
    ]

    # Обробляємо розклад
    process_schedule(posts, [youtube, facebook, twitter])
