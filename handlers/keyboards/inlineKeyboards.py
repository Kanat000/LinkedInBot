import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.messages.bot_message import lang_message
from handlers.keyboards import callback_data


def generator_industry_inline_btn(lang, page_number):
    industryInlineMarkup = InlineKeyboardMarkup(row_width=1)
    industry_arr = lang_message.get(lang).get('industries')
    if page_number == math.ceil(len(industry_arr) / 10):
        end_num = len(industry_arr)
    else:
        end_num = page_number * 7

    for i in range((page_number - 1) * 7, end_num):
        industryInlineMarkup.insert(
            InlineKeyboardButton(text=industry_arr[i], callback_data=callback_data.industry_callback.new(
                index=i
            ))
        )
    prev_btn = InlineKeyboardButton(text="\U00002B05", callback_data=callback_data.control_callback
                                    .new(status='prev', page_num=page_number))

    page_btn = InlineKeyboardButton(text=page_number, callback_data=callback_data.pageNum_callback.new(
        page_num=page_number
    ))

    next_btn = InlineKeyboardButton(text='\U000027A1', callback_data=callback_data.control_callback
                                    .new(status='next', page_num=page_number))
    industryInlineMarkup.row(
        prev_btn, page_btn, next_btn
    )
    industryInlineMarkup.insert(
        InlineKeyboardButton(text=lang_message.get(lang).get('finish'), callback_data=callback_data
                             .industry_callback.new(index='finish'))
    )
    return industryInlineMarkup


def generator_edit_account_keyboard(lang):
    edit_account_markup = InlineKeyboardMarkup(row_width=1)
    btn_arr = lang_message.get(lang).get('your_account')
    edit_account_markup.insert(
        InlineKeyboardButton(text=btn_arr[1], callback_data=callback_data
                             .edit_account_callback
                             .new(field='login'))
    )
    edit_account_markup.insert(
        InlineKeyboardButton(text=btn_arr[2], callback_data=callback_data
                             .edit_account_callback
                             .new(field='password'))
    )
    edit_account_markup.insert(
        InlineKeyboardButton(text=btn_arr[3], callback_data=callback_data
                             .edit_account_callback
                             .new(field='email'))
    )
    return edit_account_markup


def generator_industry_message(lang, arr):
    chose = ''
    for elem in arr:
        chose += elem + ', '
    text = lang_message.get(lang).get('you_chose') + '\n<b>' + chose[:-2] + '</b>\n' \
           + lang_message.get(lang).get('choose_more_industry')

    return text
