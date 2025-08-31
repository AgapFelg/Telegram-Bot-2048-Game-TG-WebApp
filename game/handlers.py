from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from inline_keyboard import game_keyboard
from game_core import Game
from models import User, Session
from sqlalchemy.orm import Session as DBSession
import numpy as np
from game_graphic import generate_image
import os

router = Router()

game = Game()

def restart_game(user_id):
    """Функция перезагрузки игры"""
    with Session() as session:
        user = session.get(User, user_id)
        # Создаем новое игровое поле
        game.field = np.zeros((4, 4), dtype=int)
        game.score = 0
        # Добавляем начальные плитки
        game.add_new_tile()
        game.add_new_tile()
        # Обновляем данные пользователя
        user.field = game.field.tolist()
        user.score = int(game.score)
        session.commit()
        # Генерируем новое изображение
        generate_image(game.field, 4, f'{user_id}.png')

def chat_move(message, direction):
    with Session() as session:
        user = session.get(User, message.from_user.id)
        game.field = np.array(user.field)
        shot_field = game.field.copy()
        if direction == 1:
            game.field = game.field.T
            game._left()
            game.field = game.field.T
        elif direction == 2:  # вправо
            game.field = np.fliplr(game.field)
            game._left()
            game.field = np.fliplr(game.field)
        elif direction == 3:  # влево
            game._left()
        elif direction == 4:  # вниз
            game.field = game.field.T
            game.field = np.fliplr(game.field)
            game._left()
            game.field = np.fliplr(game.field)
            game.field = game.field.T
        if not np.array_equal(shot_field, game.field):
            print(2)
            game.add_new_tile()

        user.field = game.field.tolist()
        user.score = int(game.score)
        session.commit()
        generate_image(game.field, 4, f'{message.from_user.id}.png')


@router.message(Command('start'))
async def start(message):
    with Session() as session:
        keyboard = game_keyboard()
        user = User(
            id=message.from_user.id,
            username=message.from_user.username,
            score=int(game.score),
            field=np.zeros((4,4), dtype=int)
        )
        game.field = np.array(user.field)
        game.add_new_tile()
        game.add_new_tile()
        user.field = game.field.tolist()
        session.add(user)
        session.commit()
        generate_image(game.field, 4, f'{message.from_user.id}.png')
        photo = FSInputFile(path=os.path.join(f'{message.from_user.id}.png'))
        await message.answer_photo(photo=photo, caption=f'Score: {game.score}', reply_markup=keyboard)


@router.callback_query(F.data == 'move_up')
async def chat_move_up(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    chat_move(callback_query, 1)
    await callback_query.answer()  # Подтверждаем callback

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    # Редактируем существующее сообщение вместо отправки нового
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=f'Score: {game.score}'
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'move_right')
async def chat_move_right(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    chat_move(callback_query, 2)
    await callback_query.answer()  # Подтверждаем callback

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    # Редактируем существующее сообщение вместо отправки нового
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=f'Score: {game.score}'
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'move_left')
async def chat_move_left(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    chat_move(callback_query, 3)
    await callback_query.answer()  # Подтверждаем callback

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    # Редактируем существующее сообщение вместо отправки нового
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=f'Score: {game.score}'
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'move_down')
async def chat_move_down(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    chat_move(callback_query, 4)
    await callback_query.answer()  # Подтверждаем callback

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    # Редактируем существующее сообщение вместо отправки нового
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=f'Score: {game.score}'
        ),
        reply_markup=keyboard
    )

@router.callback_query(F.data == 'restart')
async def chat_restart(callback_query: CallbackQuery):
    """Обработчик кнопки перезагрузки игры"""
    keyboard = game_keyboard()
    # Перезагружаем игру
    restart_game(callback_query.from_user.id)
    await callback_query.answer("Игра перезапущена!")  # Подтверждаем callback

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    # Редактируем существующее сообщение вместо отправки нового
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=f'Score: {game.score}\nИгра перезапущена!'
        ),
        reply_markup=keyboard
    )