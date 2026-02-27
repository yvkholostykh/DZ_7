import requests
import json
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import os

def ensure_data_dir():
    """Создаёт папку data/, если её нет"""
    if not os.path.exists('data'):
        os.makedirs('data')

def animate_loading():
    """Простая анимация загрузки"""
    print("🔎 Загрузка данных", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        import time
        time.sleep(0.5)
    print(" ✅ Готово!\n")

def fetch_posts():
    """Получение постов из JSONPlaceholder"""
    print("🚀 Получаем данные постов...")
    animate_loading()

    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        response.raise_for_status()
        posts = response.json()

        # Берём первые 5 постов
        first_five = posts[:5]

        # Вывод заголовков и тел
        print("📝 Первые 5 постов:\n")
        for i, post in enumerate(first_five, 1):
            print(f"📰 Пост #{i}")
            print(f"Заголовок: {post['title']}")
            print(f"Текст: {post['body']}")
            print("─" * 50)

        # Сохранение в CSV
        with open('data/posts_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'userId', 'title', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(first_five)

        print("💾 Данные постов сохранены в data/posts_data.csv")
        return first_five

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при получении постов: {e}")
        return []

def get_weather(city, posts_data):
    """Получение погоды из OpenWeatherMap"""
    print(f"\n🌤️  Получаем погоду для {city}...")
    animate_loading()

    # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ API-КЛЮЧ
    api_key = "YOUR_API_KEY"  # ← ВСТАВЬТЕ ВАШ КЛЮЧ ЗДЕСЬ!

    if api_key == "YOUR_API_KEY_HERE":
        print("❌ Пожалуйста, замените 'YOUR_API_KEY_HERE' на ваш реальный ключ из OpenWeatherMap")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }

    try:
        response = requests.get(url, params=params)

        # Обработка конкретных ошибок API
        if response.status_code == 401:
            print("❌ Ошибка 401: Неверный API-ключ. Проверьте ключ и его активацию.")
            return None
        elif response.status_code == 404:
            print(f"❌ Город '{city}' не найден. Проверьте написание.")
            return None
        elif response.status_code != 200:
            print(f"❌ Ошибка API: {response.status_code} — {response.reason}")
            return None

        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']

        # Вывод информации о погоде
        print(f"\n🌍 Город: {city}")
        print(f"🌡️  Температура: {temp}°C")
        print(f"☁️  Описание: {description.capitalize()}")

        # Сохранение отчёта в JSON
        weather_report = {
            "city": city,
            "temperature": temp,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }

        with open('data/weather_report.json', 'w', encoding='utf-8') as f:
            json.dump(weather_report, f, ensure_ascii=False, indent=2)

        print("💾 Отчёт о погоде сохранён в data/weather_report.json")

        # Создание графиков
        create_weather_plot(temp, city)
        create_combined_plot(posts_data, weather_report)  # Передаём posts_data

        return weather_report

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
        return None
    except KeyError as e:
        print(f"❌ Неверные данные от API: отсутствует поле {e}")
        return None

def create_weather_plot(temperature, city):
    """Создание графика температуры"""
    plt.figure(figsize=(8, 6))
    plt.bar([city], [temperature], color=['skyblue'])
    plt.title(f"Температура в {city}", fontsize=16, fontweight='bold')
    plt.ylabel("Температура (°C)", fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.text(0, temperature + 0.5, f"{temperature}°C", ha='center', va='bottom')

    plt.savefig('data/weather_plot.png', dpi=300, bbox_inches='tight')
    print("📊 График температуры сохранён в data/weather_plot.png")
    plt.close()

def create_combined_plot(posts, weather_data):
    """Создание комбинированного графика с постами и погодой"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # График постов (количество символов в заголовках)
    titles = [post['title'] for post in posts]
    title_lengths = [len(title) for title in titles]
    ax1.bar(range(1, 6), title_lengths, color='lightgreen')
    ax1.set_title("Длина заголовков постов")
    ax1.set_xlabel("Номер поста")
    ax1.set_ylabel("Количество символов")

    # График погоды
    ax2.bar([weather_data['city']], [weather_data['temperature']], color='orange')
    ax2.set_title("Температура")
    ax2.set_ylabel("°C")

    plt.suptitle("Анализ данных: посты и погода", fontsize=16)
    plt.savefig('data/combined_analysis.png', dpi=300, bbox_inches='tight')
    print("📊 Комбинированный график сохранён в data/combined_analysis.png")
    plt.close()

def main():
    ensure_data_dir()
    print("🎉 Добро пожаловать в проект по работе с API! 🤖")
    print("=" * 60)

    # Задание 1: Получение постов
    posts_data = fetch_posts()  # Сохраняем результат в posts_data

    # Задание 2: Получение погоды
    city = input("\n🗺️  Введите название города для проверки погоды: ").strip()
    if city:
        get_weather(city, posts_data)  # Передаём posts_data в get_weather
    else:
        print("⚠️  Город не был введён.")

    print("\n✨ Всё готово! Проверьте папку data/ для отчётов. 📁")

if __name__ == "__main__":
    main()
