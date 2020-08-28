# Тестовое задание

Скрипт использует SQLAlchemy и Postgresql 12.

Перед использованием необходимо отформатировать строку 65.

Your_password и test_database необходимо заменить.

# Запуск

    $ python3 test_project.py -s [path to file] [phone number] [step]
    
Флаг необязателен, может быть использован в любом порядке.

После запуска скрипт просит ввести API_KEY и SECRET_KEY.

Логи сохраняются в logs.txt.

Логи ошибок сохраняются в logs_errors.txt.

Logging не используется ввиду отсутствия необходимости.

В качестве уникального id в logs.txt используется timestamp.
