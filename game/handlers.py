from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from inline_keyboard import game_keyboard
from game_core import Game
from models import User, Session
import numpy as np
from game_graphic import generate_image
import os

router = Router()

game = Game()

@router.message(Command('start'))
async def start(message):
    keyboard = game_keyboard()
    user = User(
        id=message.from_user.id,
        username=message.from_user.username,
        score=0,
        field=np.zeros((4,4), dtype=int)
    )
    game.field = user.field
    game.add_new_tile()
    game.add_new_tile()
    user.field = game.field
    generate_image(game.field, 4, f'{message.from_user.id}.png')
    photo = FSInputFile(path=os.path.join(f'{message.from_user.id}.png'))
    await message.answer_photo(photo=photo, caption=f'Score: {game.score}', reply_markup=keyboard)




