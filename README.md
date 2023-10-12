# trading-robot-Tinkoff

Создаём файл .env
в этом файле будут храниться секретные токены, которые потом подставляем в 
файл creds.py

# creds.py
Необходимые библиотеки:

    tinkoff-investments


- Регистрируемся в личном кабинете в Тинькофф инвестициях.
- Создаём токен общего доступа.
- Записываем токен в переменную tok_test_all_accept, которая находится в файле .env
    Этот токен будет рабочим.
- И записываем переменную id_broker_account_all
    Этот токен будет запасным

Пример:
tok_broker_all_accept = 'YOUR TOKEN'
tok_test_all_accept = 'YOUR TOKEN'

- Далее получаем id для каждого из токенов и записываем их в переменные:
    id_broker_account_all - id для запасного токена
    id_test_account_all - id для тестового токена