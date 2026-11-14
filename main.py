import os
import requests
from dotenv import load_dotenv

# Загружаем секретный ключ из файла .env
load_dotenv()
api_key = os.getenv("API_KEY")

base_url = "https://" + "api.poiskkino.dev/v1.5/movie"
headers = {"X-API-KEY": api_key}

print("1 — Поиск фильмов по названию")
print("2 — Случайный фильм")
choice = input("Выберите действие (1 или 2): ").strip()

if choice == "1":
    query = input("Введите название фильма (например, Матрица): ").strip()
    if not query:
        print("Вы не ввели название фильма!")
        exit()

    params = {"query": query, "limit": 5}
    try:
        response = requests.get(f"{base_url}/search", params=params, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Ошибка подключения к серверу:", e)
        exit()

    data = response.json()
    movies = data.get("docs", [])

    if len(movies) == 0:
        print("По вашему запросу ничего не найдено.")
        exit()

    print("\nНайденные фильмы:")
    print("-" * 40)
    for i, movie in enumerate(movies, start=1):
        name = movie.get("name") or movie.get("alternativeName") or "Без названия"
        year = movie.get("year", "—")
        kp = (movie.get("rating") or {}).get("kp") or 0
        print(f"{i}. {name} ({year}) | Рейтинг КП: {kp:.1f}")

elif choice == "2":
    try:
        response = requests.get(f"{base_url}/random", headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Ошибка подключения к серверу:", e)
        exit()

    movie = response.json()
    name = movie.get("name") or movie.get("alternativeName") or "Без названия"
    year = movie.get("year", "—")
    kp = (movie.get("rating") or {}).get("kp") or 0
    desc = movie.get("shortDescription") or movie.get("description") or "Нет описания"

    print("-" * 40)
    print(f"Случайный фильм: {name} ({year})")
    print(f"Рейтинг Кинопоиска: {kp:.1f}")
    print(f"Описание: {desc}")
else:
    print("Неверный выбор! Запустите программу снова и введите 1 или 2.")