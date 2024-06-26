import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def get_exchange_rates(base_currency, compare_currency, start_date, end_date):
    api_key = "fa957ce08d4c47cfb1bd377982db3231"  # Замените на ваш ключ API от Open Exchange Rates
    url = f"https://openexchangerates.org/api/historical/{start_date}.json?app_id={api_key}&base={base_currency}&symbols={compare_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, что запрос успешный
        data = response.json()
        return data['rates'][compare_currency]  # Извлекаем значение для сравниваемой валюты
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return None

def create_table_and_plot(base_currency, compare_currency, period):
    today = datetime.now().date()
    start_date = today - timedelta(days=365) if period == "year" else today - timedelta(
        days=30) if period == "month" else today - timedelta(days=6)

    dates = []
    rates = []

    current_date = start_date
    while current_date <= today:
        rate_data = get_exchange_rates(base_currency, compare_currency, current_date.strftime("%Y-%m-%d"),
                                       current_date.strftime("%Y-%m-%d"))
        if rate_data is not None:
            rates.append(rate_data)
            dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    df = pd.DataFrame({"Date": dates, compare_currency: rates})

    # Создание графика
    plt.figure(figsize=(10, 6))
    plt.plot(df["Date"], df[compare_currency], marker='o')
    plt.title(f'Exchange Rate of {compare_currency} vs {base_currency}')
    plt.xlabel('Date')
    plt.ylabel(f'{compare_currency} per {base_currency}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    base_currency = input("Введите базовую валюту: ")
    compare_currency = input("Введите валюту для сравнения: ")
    period = input("Выберите период (week, month, year): ")
    create_table_and_plot(base_currency, compare_currency, period)















