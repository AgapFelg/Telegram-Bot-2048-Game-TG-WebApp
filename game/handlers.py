# импорт необходимых модулей
# импорт роутера и магического фильтра F
from aiogram import Router, F
# импорт типов данных для работы с сообщениями и callback-запросами
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
# импорт фильтра для обработки команд
from aiogram.filters import Command
# импорт функции для создания клавиатуры игры
from inline_keyboard import game_keyboard
# импорт класса игры
from game_core import Game
# импорт модели пользователя и сессии базы данных
from models import User, SessionLocal
# импорт библиотеки для работы с массивами
import numpy as np
# импорт функций для генерации изображений игрового поля
from game_graphic import generate_image, generate_image_classic
# импорт модуля для работы с операционной системой
import os

# создание роутера для обработки сообщений
router = Router()

# создание экземпляра игры
game = Game()


# функция проверки состояния игры
def check_game_state(field):
    # проверка на победу (есть плитка 2048)
    if 2048 in field:
        return "win"

    # проверка на наличие свободных клеток
    if 0 in field:
        return "continue"

    # получение размера поля
    size = field.shape[0]
    # проверка возможных ходов
    for i in range(size):
        for j in range(size):
            current = field[i, j]
            # проверка соседних клеток на возможность слияния
            if (i < size - 1 and current == field[i + 1, j]) or (j < size - 1 and current == field[i, j + 1]):
                return "continue"

    # если ходов нет - игра окончена
    return "game_over"


# функция для получения сессии базы данных
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# функция перезапуска игры
def restart_game(user_id):
    # создание сессии базы данных
    session = SessionLocal()
    try:
        # получение пользователя по id
        user = session.get(User, user_id)
        # сброс игрового поля
        game.field = np.zeros((4, 4), dtype=int)
        # сброс счета
        game.score = 0
        # добавление двух начальных плиток
        game.add_new_tile()
        game.add_new_tile()
        # обновление поля пользователя
        user.field = game.field.tolist()
        # обновление счета пользователя
        user.score = int(game.score)
        # сохранение изменений
        session.commit()
        # генерация изображения в зависимости от темы
        if user.theme == 'classic':
            generate_image_classic(game.field, 4, f'{user_id}.png')
        else:
            generate_image(game.field, 4, f'{user_id}.png')
        # возврат рекорда и темы
        return user.height_score, user.theme
    finally:
        # закрытие сессии
        session.close()


# функция обработки хода
def chat_move(message, direction):
    game_state = "continue"
    high_score = 0
    theme = 'classic'
    # создание сессии базы данных
    session = SessionLocal()
    try:
        # получение пользователя по id
        user = session.get(User, message.from_user.id)
        # восстановление игрового поля из базы данных
        game.field = np.array(user.field)
        # восстановление счета из базы данных
        game.score = user.score
        theme = user.theme
        # сохранение копии поля для сравнения
        shot_field = game.field.copy()

        # обработка движения вверх
        if direction == 1:
            game.field = game.field.T
            game._left()
            game.field = game.field.T
        # обработка движения вправо
        elif direction == 2:
            game.field = np.fliplr(game.field)
            game._left()
            game.field = np.fliplr(game.field)
        # обработка движения влево
        elif direction == 3:
            game._left()
        # обработка движения вниз
        elif direction == 4:
            game.field = game.field.T
            game.field = np.fliplr(game.field)
            game._left()
            game.field = np.fliplr(game.field)
            game.field = game.field.T

        # проверка изменения поля после хода
        if not np.array_equal(shot_field, game.field):
            # добавление новой плитки если поле изменилось
            game.add_new_tile()
            # проверка состояния игры
            game_state = check_game_state(game.field)

        # обновление поля пользователя
        user.field = game.field.tolist()
        # обновление счета пользователя
        user.score = int(game.score)
        # обновление рекорда если текущий счет больше
        if user.score > user.height_score:
            user.height_score = user.score
        high_score = user.height_score
        # сохранение изменений
        session.commit()
        # генерация изображения в зависимости от темы
        if theme == 'classic':
            generate_image_classic(game.field, 4, f'{message.from_user.id}.png')
        else:
            generate_image(game.field, 4, f'{message.from_user.id}.png')

    finally:
        # закрытие сессии
        session.close()

    # возврат состояния игры, рекорда и темы
    return game_state, high_score, theme


# обработчик команды /start
@router.message(Command('start'))
async def start(message):
    # создание сессии базы данных
    session = SessionLocal()
    try:
        # создание клавиатуры игры
        keyboard = game_keyboard()
        # получение пользователя по id
        user = session.get(User, message.from_user.id)

        # создание нового пользователя если не существует
        if user is None:
            user = User(
                id=message.from_user.id,
                username=message.from_user.username,
                score=0,
                field=np.zeros((4, 4), dtype=int).tolist(),
                height_score=0,
                theme='classic'
            )
            # инициализация игрового поля
            game.field = np.zeros((4, 4), dtype=int)
            game.score = 0
            # добавление двух начальных плиток
            game.add_new_tile()
            game.add_new_tile()
            # обновление поля пользователя
            user.field = game.field.tolist()
            # обновление счета пользователя
            user.score = int(game.score)
            # добавление пользователя в сессию
            session.add(user)
            # сохранение изменений
            session.commit()
        else:
            # восстановление состояния игры из базы данных
            game.field = np.array(user.field)
            game.score = user.score

        # генерация изображения в зависимости от темы
        if user.theme == 'classic':
            generate_image_classic(game.field, 4, f'{message.from_user.id}.png')
        else:
            generate_image(game.field, 4, f'{message.from_user.id}.png')

        # формирование подписи к изображению
        theme_name = "классическая" if user.theme == 'classic' else "черно-белая"
        caption = f'Score: {game.score}\nHigh Score: {user.height_score}\nТема: {theme_name}'
        # проверка состояния игры
        game_state = check_game_state(game.field)
        if game_state == "win":
            caption += "\n🎉🎉🎉Победа, че🎉🎉🎉"
        elif game_state == "game_over":
            caption += "\n💀💀💀ГГ! СЛИТ!💀💀💀"

        # создание объекта файла изображения
        photo = FSInputFile(path=os.path.join('uploads', f'{message.from_user.id}.png'))
        # отправка изображения с клавиатурой
        await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard)
    finally:
        # закрытие сессии
        session.close()


# обработчик движения вверх
@router.callback_query(F.data == 'move_up')
async def chat_move_up(callback_query: CallbackQuery):
    # создание клавиатуры
    keyboard = game_keyboard()
    # обработка хода
    game_state, high_score, theme = chat_move(callback_query, 1)
    # подтверждение получения callback
    await callback_query.answer()

    # формирование подписи
    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉🎉🎉Победа, че🎉🎉🎉"
    elif game_state == "game_over":
        caption += "\n💀💀💀ГГ! СЛИТ!💀💀💀"

    # создание объекта файла изображения
    photo = FSInputFile(path=os.path.join('uploads', f'{callback_query.from_user.id}.png'))
    # редактирование сообщения с новым изображением
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


# обработчик движения вправо
@router.callback_query(F.data == 'move_right')
async def chat_move_right(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 2)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉🎉🎉Победа, че🎉🎉🎉"
    elif game_state == "game_over":
        caption += "\n💀💀💀ГГ! СЛИТ!💀💀💀"

    photo = FSInputFile(path=os.path.join('uploads', f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


# обработчик движения влево
@router.callback_query(F.data == 'move_left')
async def chat_move_left(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 3)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉🎉🎉Победа, че🎉🎉🎉"
    elif game_state == "game_over":
        caption += "\n💀💀💀ГГ! СЛИТ!💀💀💀"

    photo = FSInputFile(path=os.path.join('uploads', f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


# обработчик движения вниз
@router.callback_query(F.data == 'move_down')
async def chat_move_down(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 4)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉🎉🎉Победа, че🎉🎉🎉"
    elif game_state == "game_over":
        caption += "\n💀💀💀ГГ! СЛИТ!💀💀💀"

    photo = FSInputFile(path=os.path.join('uploads', f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


# обработчик перезапуска игры
@router.callback_query(F.data == 'restart')
async def chat_restart(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    # перезапуск игры
    high_score, theme = restart_game(callback_query.from_user.id)
    # уведомление пользователя
    await callback_query.answer("Игра перезапущена!")

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}\nИгра перезапущена!'

    photo = FSInputFile(path=os.path.join('uploads', f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


# обработчик смены темы
@router.callback_query(F.data == 'change_theme')
async def chat_change_theme(callback_query: CallbackQuery):
    keyboard = game_keyboard()

    session = SessionLocal()
    try:
        user = session.get(User, callback_query.from_user.id)
        # переключение темы
        if user.theme == 'classic':
            user.theme = 'bw'
        else:
            user.theme = 'classic'

        # генерация изображения в новой теме
        if user.theme == 'classic':
            generate_image_classic(np.array(user.field), 4, f'{callback_query.from_user.id}.png')
        else:
            generate_image(np.array(user.field), 4, f'{callback_query.from_user.id}.png')

        session.commit()

        theme_name = "классическая" if user.theme == 'classic' else "черно-белая"
        # уведомление пользователя
        await callback_query.answer(f"Тема изменена на: {theme_name}")

        caption = f'Score: {user.score}\nHigh Score: {user.height_score}\nТема: {theme_name}'

        photo = FSInputFile(path=os.path.join('uploads', f'{callback_query.from_user.id}.png'))
        # обновление сообщения с новой темой
        await callback_query.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=keyboard
        )
    finally:
        session.close()