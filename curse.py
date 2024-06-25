import requests

base_currency = input("Введите код первичной валюты: ")
target_currency = input("Введите код целевой валюты: ")

amount = float(input("Введите сумму первичной валюты: "))

url = f"https://v6.exchangerate-api.com/v6/01f5596ca1a5b5081ae31e99/latest/{base_currency}"
response = requests.get(url)

if response.status_code == 200:
    exchange_rates = response.json()["conversion_rates"]
    if target_currency in exchange_rates:
        target_rate = exchange_rates[target_currency]
        converted_amount = amount * target_rate
        print("Итоговая сумма:", converted_amount, target_currency)
    else:
        print("Целевая валюта не найдена.")
else:
    print("Ошибка при получении данных о курсах валют.")
