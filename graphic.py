import requests
from datetime import datetime, timedelta
import pandas as pd
from IPython.display import display


def get_all_currencies():
    url = "https://v6.exchangerate-api.com/v6/01f5596ca1a5b5081ae31e99/currency"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        currencies = [(currency['code'], currency['name']) for currency in data['currencies']]
        return currencies
    else:
        print("Ошибка при получении списка валют")
        return []


def get_target_currency(currencies):
    print("Выберите целевую валюту из списка:")
    for i, (code, name) in enumerate(currencies, start=1):
        print(f"{i}. {name} ({code})")
    choice = int(input("Введите номер выбранной валюты: ")) - 1
    return currencies[choice][0]


def get_exchange_rates(base_currency, target_currency, year, month, day):
    url = f"https://v6.exchangerate-api.com/v6/01f5596ca1a5b5081ae31e99/history/{base_currency}/{target_currency}/{year}/{month}/{day}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['conversion_rates']
    else:
        print("Ошибка при получении данных о курсах валют")
        return {}


def filter_data_by_period(base_currency, target_currency, period):
    today = datetime.now().strftime('%Y-%m-%d')

    if period.lower() == 'неделя':
        start_date = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
        end_date = today
    elif period.lower() == 'месяц':
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today
    elif period.lower() == 'год':
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        end_date = today
    else:
        print("Неверный период. Пожалуйста, выберите неделю, месяц или год.")
        return {}

    # Получаем данные за последние 30 дней для месяца и года, а за последние 7 дней для недели
    if period.lower() != 'неделя':
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=29)).strftime('%Y-%m-%d')

    # Здесь мы используем end_date для запроса, так как API может не поддерживать запрос к конкретным датам без указания конкретного числа месяца и года
    rates = get_exchange_rates(base_currency, target_currency, end_date.split('-')[0], end_date.split('-')[1],
                               end_date.split('-')[2])
    filtered_dates = [date.strftime('%Y-%m-%d') for date in pd.date_range(start=start_date, end=end_date, freq='D')]

    filtered_data = {date: rates[date] for date in filtered_dates if date in rates}
    return filtered_data


def display_table(data):
    if data:
        df = pd.DataFrame(list(data.items()), columns=['Date', 'Exchange Rate'])
        display(df)
    else:
        print("Данные не найдены.")


# Пример использования
if __name__ == "__main__":
    currencies = get_all_currencies()
    if not currencies:
        exit(1)

    base_currency = input("Введите базовую валюту: ").upper()
    target_currency = get_target_currency(currencies)
    period = input("Введите период (неделя, месяц, год): ").lower()

    if period not in ['неделя', 'месяц', 'год']:
        print("Неверный период. Пожалуйста, выберите неделю, месяц или год.")
    else:
        data = filter_data_by_period(base_currency, target_currency, period)
        display_table(data)
























