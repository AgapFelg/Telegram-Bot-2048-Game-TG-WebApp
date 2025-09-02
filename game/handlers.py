from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from inline_keyboard import game_keyboard
from game_core import Game
from models import User, SessionLocal
import numpy as np
from game_graphic import generate_image, generate_image_classic
import os

router = Router()

game = Game()


def check_game_state(field):
    if 2048 in field:
        return "win"

    if 0 in field:
        return "continue"

    size = field.shape[0]
    for i in range(size):
        for j in range(size):
            current = field[i, j]
            if (i < size - 1 and current == field[i + 1, j]) or (j < size - 1 and current == field[i, j + 1]):
                return "continue"

    return "game_over"


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def restart_game(user_id):
    session = SessionLocal()
    try:
        user = session.get(User, user_id)
        game.field = np.zeros((4, 4), dtype=int)
        game.score = 0
        game.add_new_tile()
        game.add_new_tile()
        user.field = game.field.tolist()
        user.score = int(game.score)
        session.commit()
        if user.theme == 'classic':
            generate_image_classic(game.field, 4, f'{user_id}.png')
        else:
            generate_image(game.field, 4, f'{user_id}.png')
        return user.height_score, user.theme
    finally:
        session.close()


def chat_move(message, direction):
    game_state = "continue"
    high_score = 0
    theme = 'classic'
    session = SessionLocal()
    try:
        user = session.get(User, message.from_user.id)
        game.field = np.array(user.field)
        game.score = user.score
        theme = user.theme
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
            game.add_new_tile()
            game_state = check_game_state(game.field)

        user.field = game.field.tolist()
        user.score = int(game.score)
        if user.score > user.height_score:
            user.height_score = user.score
        high_score = user.height_score
        session.commit()
        if theme == 'classic':
            generate_image_classic(game.field, 4, f'{message.from_user.id}.png')
        else:
            generate_image(game.field, 4, f'{message.from_user.id}.png')

    finally:
        session.close()

    return game_state, high_score, theme


@router.message(Command('start'))
async def start(message):
    session = SessionLocal()
    try:
        keyboard = game_keyboard()
        user = session.get(User, message.from_user.id)

        if user is None:
            user = User(
                id=message.from_user.id,
                username=message.from_user.username,
                score=0,
                field=np.zeros((4, 4), dtype=int).tolist(),
                height_score=0,
                theme='classic'
            )
            game.field = np.zeros((4, 4), dtype=int)
            game.score = 0
            game.add_new_tile()
            game.add_new_tile()
            user.field = game.field.tolist()
            user.score = int(game.score)
            session.add(user)
            session.commit()
        else:
            game.field = np.array(user.field)
            game.score = user.score

        if user.theme == 'classic':
            generate_image_classic(game.field, 4, f'{message.from_user.id}.png')
        else:
            generate_image(game.field, 4, f'{message.from_user.id}.png')

        theme_name = "классическая" if user.theme == 'classic' else "черно-белая"
        caption = f'Score: {game.score}\nHigh Score: {user.height_score}\nТема: {theme_name}'
        game_state = check_game_state(game.field)
        if game_state == "win":
            caption += "\n🎉🎉🎉Победа, че🎉🎉🎉"
        elif game_state == "game_over":
            caption += "\n💀💀💀ГГ! СЛИТ!💀💀💀"

        photo = FSInputFile(path=os.path.join(f'{message.from_user.id}.png'))
        await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard)
    finally:
        session.close()


@router.callback_query(F.data == 'move_up')
async def chat_move_up(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 1)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉 Победа! Вы набрали 2048!"
    elif game_state == "game_over":
        caption += "\n💀 Игра окончена! Нет возможных ходов."

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'move_right')
async def chat_move_right(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 2)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉 Победа! Вы набрали 2048!"
    elif game_state == "game_over":
        caption += "\n💀 Игра окончена! Нет возможных ходов."

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'move_left')
async def chat_move_left(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 3)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉 Победа! Вы набрали 2048!"
    elif game_state == "game_over":
        caption += "\n💀 Игра окончена! Нет возможных ходов."

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'move_down')
async def chat_move_down(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    game_state, high_score, theme = chat_move(callback_query, 4)
    await callback_query.answer()

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}'
    if game_state == "win":
        caption += "\n🎉 Победа! Вы набрали 2048!"
    elif game_state == "game_over":
        caption += "\n💀 Игра окончена! Нет возможных ходов."

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'restart')
async def chat_restart(callback_query: CallbackQuery):
    keyboard = game_keyboard()
    high_score, theme = restart_game(callback_query.from_user.id)
    await callback_query.answer("Игра перезапущена!")

    theme_name = "классическая" if theme == 'classic' else "черно-белая"
    caption = f'Score: {game.score}\nHigh Score: {high_score}\nТема: {theme_name}\nИгра перезапущена!'

    photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'change_theme')
async def chat_change_theme(callback_query: CallbackQuery):
    keyboard = game_keyboard()

    session = SessionLocal()
    try:
        user = session.get(User, callback_query.from_user.id)
        if user.theme == 'classic':
            user.theme = 'bw'
        else:
            user.theme = 'classic'

        if user.theme == 'classic':
            generate_image_classic(np.array(user.field), 4, f'{callback_query.from_user.id}.png')
        else:
            generate_image(np.array(user.field), 4, f'{callback_query.from_user.id}.png')

        session.commit()

        theme_name = "классическая" if user.theme == 'classic' else "черно-белая"
        await callback_query.answer(f"Тема изменена на: {theme_name}")

        caption = f'Score: {user.score}\nHigh Score: {user.height_score}\nТема: {theme_name}'

        photo = FSInputFile(path=os.path.join(f'{callback_query.from_user.id}.png'))
        await callback_query.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption
            ),
            reply_markup=keyboard
        )
    finally:
        session.close()