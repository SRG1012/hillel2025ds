import random
import string
import time
import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API_KEY = os.getenv("ALPHAVANTAGE_KEY_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def random_string(n: int) -> str:
    return "".join((random.choice(string.ascii_letters) for _ in range(n)))


@app.get("/fetch-market")
def fetch_market():
    """
    User Request:           None
    User Response:          str

    Alphavantage Request:   dict
    Alphavantage Response:  dict
    {'Realtime Currency Exchange Rate': {'1. From_Currency Code': 'UAH',
             '2. From_Currency Name': 'Ukrainian '
                                      'Hryvnia',
             '3. To_Currency Code': 'USD',
             '4. To_Currency Name': 'United States '
                                    'Dollar',
             '5. Exchange Rate': '0.02380000',
             '6. Last Refreshed': '2025-01-06 19:37:43',
             '7. Time Zone': 'UTC',
             '8. Bid Price': '0.02379000',
             '9. Ask Price': '0.02380000'}
    }
    """

    url = (
        "https://www.alphavantage.co/query?"
        "function=CURRENCY_EXCHANGE_RATE&"
        "from_currency=UAH&"
        f"to_currency=USD&apikey={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

    time.sleep(3)
    return {"rate": rate}


@app.get("/article-idea")
def article_idea():
    time.sleep(5)
    return {
        "title": random_string(10),
        "idea": random_string(30),
    }