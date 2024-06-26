import requests

base_currency = input("Введите код первичной валюты: ")
target_currency = input("Введите код целевой валюты: ")

amount = float(input("Введите сумму первичной валюты: "))

# Open Exchange Rates API endpoint
url = f"https://openexchangerates.org/api/latest.json?app_id=fa957ce08d4c47cfb1bd377982db3231"
response = requests.get(url)

if response.status_code == 200:
    # Accessing the exchange rates from the response
    exchange_rates = response.json()["rates"]
    if target_currency in exchange_rates:
        target_rate = exchange_rates[target_currency]
        converted_amount = amount * target_rate
        print("Итоговая сумма:", converted_amount, target_currency)
    else:
        print("Целевая валюта не найдена.")
else:
    print("Ошибка при получении данных о курсах валют.")
