# CryptoSpotty Floor Bot

Классный бот, который сообщает актуальный флор коллекции в беседе ВКонтакте.

## Установка
Установить зависимоcти:
```sh
py -m venv venv
pip install -r requirements.txt
```
Переименуйте файл example.env в .env и замените текст YOUR_VK_API_KEY на токен группы ВКонтакте, где будет запущен бот.

## Запуск
```sh
py main.py
```

## Использование
Ниже находится список доступных команд
### Админские команды
- /старт N -- запустить автоматическую рассылку в беседе. N = задержка между отправкой рассылки в минутах.
- /стоп -- остановить рассылку.

### Пользовательские команды
- /флор -- получить актуальный флор коллекции.

## TODO
- Избавиться от богомерзкой глобальной переменной
- Сделать локальное сохранение peer_id беседы с запущенным ботом
- Сделать отдельный поточек для отправки рассылки