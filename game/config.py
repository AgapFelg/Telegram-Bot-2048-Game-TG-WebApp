# импорт класса Env из библиотеки environs для работы
# с .env (переменными окружения)
from environs import Env

# инициализация объекта класса Env()
env = Env()
# чтение переменных окружения
env.read_env()

# создание класса конфига
class Config:
    def __init__(self):
        # читает токен бота
        self.bot_token = env('BOT_TOKEN')
        # читает строку подключения к БД
        self.database_uri = env('DATABASE_URI')