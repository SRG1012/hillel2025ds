import random
import string
import time
import os
import abc
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

API_KEY = os.getenv("ALPHAVANTAGE_KEY_API_KEY")


app = FastAPI()

# Додаткові налаштування CORS для взаємодії з фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationService(abc.ABC):

    @abc.abstractmethod
    async def generate_random_article_idea(self):
        ...

    @abc.abstractmethod
    async def generate_technical_guide(self):
        ...

    @abc.abstractmethod
    async def generate_fiction(self):
        ...


def _random_string(n: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


class ArticleGenerationService(GenerationService):

    async def generate_random_article_idea(self):
        """Генерує випадкову ідею для статті."""
        title = _random_string(10)
        idea = _random_string(30)
        await asyncio.sleep(1)
        return {"title": title, "idea": idea}

    async def generate_technical_guide(self):
        """Генерує випадкову технічну статтю."""
        title = "Technical Guide: " + _random_string(8)
        content = _random_string(50)
        await asyncio.sleep(1)
        return {"title": title, "content": content}

    async def generate_fiction(self):
        title = "Fiction Story: " + _random_string(12)
        story = _random_string(100)
        await asyncio.sleep(1)
        return {"title": title, "story": story}


# Ініціалізація сервісу генерації статей
article_service = ArticleGenerationService()


@app.get("/fetch-market")
async def fetch_market():

    url = (
        "https://www.alphavantage.co/query?"
        "function=CURRENCY_EXCHANGE_RATE&"
        "from_currency=UAH&"
        f"to_currency=USD&apikey={API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    rate = data["Realtime Currency Exchange Rate"].get("5. Exchange Rate", "N/A")
    return {"rate": rate}


@app.get("/article-idea")
async def article_idea():

    article = await article_service.generate_random_article_idea()
    return article
