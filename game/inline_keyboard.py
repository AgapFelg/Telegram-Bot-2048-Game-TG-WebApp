# импорт классов для создания inline-клавиатуры из aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import Config

config = Config()

# функция создания игровой клавиатуры
def game_keyboard():
    # создание пустого списка для кнопок
    buttons = []

    # создание первой строки с одной кнопкой движения вверх
    control_row_1 = [
        InlineKeyboardButton(text='⬆️', callback_data='move_up')
        # создание кнопки со стрелкой вверх и callback_data 'move_up'
    ]

    # создание второй строки с двумя кнопками движения влево и вправо
    control_row_2 = [
        InlineKeyboardButton(text='⬅️', callback_data='move_left'),
        # создание кнопки со стрелкой влево и callback_data 'move_left'
        InlineKeyboardButton(text='➡️', callback_data='move_right')
        # создание кнопки со стрелкой вправо и callback_data 'move_right'
    ]

    # создание третьей строки с одной кнопкой движения вниз
    control_row_3 = [
        InlineKeyboardButton(text='⬇️', callback_data='move_down')
        # создание кнопки со стрелкой вниз и callback_data 'move_down'
    ]

    # создание четвертой строки с кнопками перезапуска и смены темы
    control_row_4 = [
        InlineKeyboardButton(text='🔄', callback_data='restart'),
        # создание кнопки с иконкой обновления и callback_data 'restart'
        InlineKeyboardButton(text='🎨', callback_data='change_theme')
        # создание кнопки с иконкой палитры и callback_data 'change_theme'
    ]

    # создание пятой строки с кнопкой входа в веб приложение
    control_row_5 = [
        InlineKeyboardButton(text='web_app', web_app=WebAppInfo(url=config.web_app_url))
    ]

    # добавление всех строк кнопок в основной список
    buttons.append(control_row_1)
    buttons.append(control_row_2)
    buttons.append(control_row_3)
    buttons.append(control_row_4)
    buttons.append(control_row_5)

    # создание и возврат клавиатуры на основе списка кнопок
    return InlineKeyboardMarkup(inline_keyboard=buttons)