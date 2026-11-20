import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

BASE_URL = "https://" + "api.poiskkino.dev/v1.5/movie"
HEADERS = {"X-API-KEY": api_key}

def get_json(url, params=None):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Не получилось загрузить данные: {e}")
        return None

while True:
    print("\n1 — Поиск фильмов   2 — Случайный фильм   0 — Выход")
    choice = input("> ").strip()

    if choice == "0":
        break

    elif choice == "1":
        query = input("Введите название фильма (например, Матрица): ").strip()
        if not query:
            continue

        page = 1
        while True:
            params = {"query": query, "page": page, "limit": 5}
            data = get_json(f"{BASE_URL}/search", params)
            if data is None:
                break

            movies = data.get("docs", [])
            if not movies:
                print("Ничего не найдено.")
                break

            print(f"\n--- Страница {page} ---")
            for i, m in enumerate(movies, start=1):
                name = m.get("name") or m.get("alternativeName") or "Без названия"
                year = m.get("year", "—")
                kp = (m.get("rating") or {}).get("kp") or 0
                print(f"{i}. {name} ({year}) | Рейтинг КП: {kp:.1f}")
            print("-" * 30)

            if page < data.get("pages", 1):
                more = input("Показать ещё? (да/нет): ").strip().lower()
                if more == "да":
                    page += 1
                else:
                    break
            else:
                break

    elif choice == "2":
        movie = get_json(f"{BASE_URL}/random")
        if movie:
            name = movie.get("name") or movie.get("alternativeName") or "Без названия"
            year = movie.get("year", "—")
            kp = (movie.get("rating") or {}).get("kp") or 0
            desc = movie.get("shortDescription") or movie.get("description") or "Нет описания"
            print("-" * 30)
            print(f"{name} ({year}) | Рейтинг КП: {kp:.1f}")
            print(f"Описание: {desc}")
            print("-" * 30)
