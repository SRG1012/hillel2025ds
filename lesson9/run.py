import argparse
import asyncio
import time
import random
import httpx
import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]

# Синхронна функція для отримання даних за допомогою requests
def sync_pokemons():
    urls = get_urls(n=50)
    results = []
    for url in urls:
        print(f"Виконується запит {url} за допомогою requests")
        response = requests.get(url)
        response.raise_for_status()
        results.append(response.json()["name"])
    return results

# Асинхронна функція для отримання даних за допомогою httpx
async def async_pokemons():
    urls = get_urls(n=50)
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        results = [response.json()["name"] for response in responses]
    return results

def main():
    parser = argparse.ArgumentParser(description="Отримання імен Покемонів за допомогою requests або httpx.")
    parser.add_argument(
        "library",
        choices=["requests", "httpx"],
        help="Вкажіть бібліотеку для отримання даних.",
    )

    args = parser.parse_args()

    start = time.perf_counter()

    if args.library == "httpx":
        data = asyncio.run(async_pokemons())
    elif args.library == "requests":
        data = sync_pokemons()

    end = time.perf_counter()

    print(data)
    print(f"Довжина колекції: {len(data)}")
    print(f"Час виконання: {end - start:.2f} секунд")

if __name__ == "__main__":
    raise SystemExit(main())
