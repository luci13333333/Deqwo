import json
import hashlib

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функция для проверки пароля
def check_password(hashed_password, plain_password):
    return hashed_password == hash_password(plain_password)

# Функция для чтения данных из файла
def read_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Функция для записи данных в файл
def write_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Функция для запроса данных от пользователя
def get_user_input():
    username = input("Введите имя пользователя: ")
    email = input("Введите электронную почту: ")
    phone = input("Введите номер телефона: ")
    password = input("Введите пароль: ")
    return username, email, phone, password

# Функция для регистрации нового пользователя
def register_user(account_file='Account.txt'):
    username, email, phone, password = get_user_input()
    hashed_password = hash_password(password)
    new_user = {'username': username, 'email': email, 'phone': phone, 'password': hashed_password}
    current_users = read_data(account_file)
    current_users[username] = new_user
    write_data(current_users, account_file)
    print("Регистрация успешно завершена.")

# Функция для входа пользователя
def login_user(account_file='Account.txt'):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    current_users = read_data(account_file)
    if username in current_users and check_password(current_users[username]['password'], password):
        print("Успешный вход")
    else:
        print("Неверные учетные данные")

# Главная функция программы
def main():
    while True:
        print("\nВыберите действие:")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")
        choice = input("Введите номер действия: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()


