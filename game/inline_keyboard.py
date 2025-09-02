from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def game_keyboard():

    buttons = []

    control_row_1 = [
        InlineKeyboardButton(text='⬆️', callback_data='move_up')
    ]
    control_row_2 = [
        InlineKeyboardButton(text='⬅️', callback_data='move_left'),
        InlineKeyboardButton(text='➡️', callback_data='move_right')
    ]
    control_row_3 = [
        InlineKeyboardButton(text='⬇️', callback_data='move_down')
    ]
    control_row_4 = [
        InlineKeyboardButton(text='🔄', callback_data='restart'),
        InlineKeyboardButton(text='🎨', callback_data='change_theme')
    ]

    buttons.append(control_row_1)
    buttons.append(control_row_2)
    buttons.append(control_row_3)
    buttons.append(control_row_4)

    return InlineKeyboardMarkup(inline_keyboard=buttons)