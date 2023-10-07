from tinkoff.invest import Client
from decouple import config

# токен для общего доступа к брокерскому счёту
tok_broker_all_accept = config('tok_broker_all_accept', default='')

# токен для общего доступа к тестовому счёту
tok_test_all_accept = config('tok_test_all_accept', default='')


# подключаемся к брокерсскому счёту
with Client(tok_broker_all_accept) as client_broker:

    # id брокерского счёта клиента
    id_broker_account_all = client_broker.users.get_accounts().accounts[0].id


# подключаемся к API для инициализации данных и переноса его потом в другие модули
with Client(tok_test_all_accept) as client_test:

    # id тестового счёта клиента
    id_test_account_all = client_test.users.get_accounts().accounts[0].id

def open_api():
    with Client(tok_test_all_accept) as client:
        pass

    return client
