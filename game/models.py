# импорт необходимых компонентов из sqlalchemy
from sqlalchemy import Column, Integer, String, JSON, create_engine, BigInteger
# импорт декларативной базы для создания моделей
from sqlalchemy.ext.declarative import declarative_base
# импорт sessionmaker для создания сессий базы данных
from sqlalchemy.orm import sessionmaker
# импорт класса конфигурации из файла config.py
from config import Config

# создание экземпляра конфигурации
config = Config()

# создание движка (engine) для подключения к базе данных
# использует uri базы данных из конфигурации
engine = create_engine(config.database_uri)
# создание фабрики сессий с настройками:
# autocommit=False - автоматическое подтверждение изменений отключено
# autoflush=False - автоматическая синхронизация отключена
# bind=engine - привязка к созданному движку
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# создание базового класса для всех моделей
Base = declarative_base()

# определение модели пользователя
class User(Base):
    # имя таблицы в базе данных
    __tablename__ = 'users'

    # определение колонок таблицы:

    # id пользователя (big integer, первичный ключ)
    id = Column(BigInteger, primary_key=True)
    # имя пользователя (строка)
    username = Column(String)
    # текущий счет (целое число, значение по умолчанию 0)
    score = Column(Integer, default=0)
    # рекордный счет (целое число, значение по умолчанию 0)
    height_score = Column(Integer, default=0)
    # игровое поле в формате json (список, значение по умолчанию пустой список)
    field = Column(JSON, default=list)
    # тема оформления (строка, значение по умолчанию 'classic')
    theme = Column(String, default='classic')

# создание всех таблиц в базе данных на основе определенных моделей
# bind=engine - указание движка для создания таблиц
Base.metadata.create_all(bind=engine)