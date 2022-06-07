from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.messages.bot_message import lang_message

lang_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
lang_keyboard.insert(
    KeyboardButton(text='\U0001F1F7\U0001F1FA Русский')
)
lang_keyboard.insert(
    KeyboardButton(text='\U0001F1EC\U0001F1E7 Engilsh')
)


def generator_main_keyboards(lang):
    main_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for btn in lang_message.get(lang).get('main_keyboard'):
        main_keyboard.insert(
            KeyboardButton(text=btn)
        )
    return main_keyboard


def generator_filter_keyboards(lang):
    filter_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    filter_keyboard.insert(
        KeyboardButton(text=lang_message.get(lang).get('by_company'))
    )
    filter_keyboard.insert(
        KeyboardButton(text=lang_message.get(lang).get('by_industry'))
    )
    filter_keyboard.insert(
        KeyboardButton(text=lang_message.get(lang).get('by_position'))
    )
    filter_keyboard.insert(
        KeyboardButton(text=lang_message.get(lang).get('by_region'))
    )
    filter_keyboard.insert(
        KeyboardButton(text=lang_message.get(lang).get('finish'))
    )
    return filter_keyboard


def generator_cancel_keyboard(lang):
    cancel_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cancel_keyboard.insert(
        KeyboardButton(lang_message.get(lang).get('cancel'))
    )
    return cancel_keyboard


def generator_industry_keyboard(lang):
    industry_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for industry in lang_message.get(lang).get('industries'):
        industry_keyboard.insert(
            KeyboardButton(industry)
        )
    industry_keyboard.insert(
        KeyboardButton(lang_message.get(lang).get('cancel'))
    )
    return industry_keyboard


def generator_last_keyboard(lang):
    last_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in lang_message.get(lang).get('last_keyboard_buttons'):
        last_keyboard.insert(
            KeyboardButton(button)
        )
    return last_keyboard

