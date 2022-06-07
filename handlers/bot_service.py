import math

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, LabeledPrice, PreCheckoutQuery

from config import dbName, provider_token
from database import dbConnection
from handlers.mailSender import send_email
from loader import dp, bot
from handlers.messages.bot_message import lang_message
from handlers.keyboards import replyKeyboards, inlineKeyboards

db = dbConnection.Sqlite(dbName)


class Form(StatesGroup):
    language = State()
    edit_account_field = State()
    companies = State()
    industries = State()
    position = State()
    region = State()
    sms = State()
    login = State()
    password = State()
    email = State()


async def send_invoice_for_payment(message, lang):
    prices = [
        LabeledPrice(label=lang_message.get(lang).get('payment_title'), amount=50000)
    ]
    await bot.send_invoice(message.chat.id,
                           title=lang_message.get(lang).get('payment_title'),
                           description=lang_message.get(lang).get('payment_description'),
                           provider_token=provider_token,
                           currency='rub',
                           is_flexible=False,
                           prices=prices,
                           payload='Custom-Payload'
                           )


@dp.message_handler(Command('start'))
async def start_bot(message: Message):
    chat_id = message.chat.id
    if db.exists_user(chat_id):
        lang = db.get_user(chat_id)[5]
        if db.is_paid(message.chat.id):
            await message.answer(text=lang_message.get(lang).get('start'),
                                 reply_markup=replyKeyboards.generator_main_keyboards(lang))
        else:
            await send_invoice_for_payment(message, lang)
    else:
        db.create_row(chat_id)
        await send_invoice_for_payment(message, 'ru')


@dp.pre_checkout_query_handler(lambda query: True)
async def process_payment(pre_checkout_query: PreCheckoutQuery):
    if pre_checkout_query.invoice_payload != 'Custom-Payload':
        await bot.answer_pre_checkout_query(pre_checkout_query.id,
                                            ok=False, error_message="Something went wrong...")
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=['successful_payment'])
async def success_payment(message: Message):
    db.update_paid(message.chat.id, 'true')
    lang = db.get_user(message.chat.id)[5]
    await message.answer(text=lang_message.get(lang).get('start'),
                         reply_markup=replyKeyboards.generator_main_keyboards(lang))


@dp.message_handler(Command('new_mailing'))
@dp.message_handler(text='Новая рассылка')
@dp.message_handler(text='New mailing')
async def new_mailing(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_user(chat_id)[5]
    if db.is_paid(message.chat.id):
        async with state.proxy() as data:
            data['companies'] = []
            data['industries'] = []
            data['region'] = []
            data['position'] = []
            data['sms'] = ""
            data['login'] = db.get_user(message.chat.id)[3]
            data['password'] = db.get_user(message.chat.id)[4]
            data['email'] = db.get_user(message.chat.id)[5]

        await message.answer(text=lang_message.get(lang).get('new_mailing'),
                             reply_markup=replyKeyboards.generator_filter_keyboards(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(text='По компаниям')
@dp.message_handler(text='By company')
async def form_company_set(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await Form.companies.set()
        await message.answer(text=lang_message.get(lang).get('write_company'),
                             reply_markup=replyKeyboards.generator_cancel_keyboard(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(state=Form.companies)
async def write_company(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        if message.text != lang_message.get(lang).get('cancel'):
            data['companies'] += message.text.split(',')
            await state.finish()
            await message.answer(text=lang_message.get(lang).get('choose_category'),
                                 reply_markup=replyKeyboards.generator_filter_keyboards(lang))
        else:
            await state.finish()
            await message.answer(text=lang_message.get(lang).get('clicked_cancel'),
                                 reply_markup=replyKeyboards.generator_filter_keyboards(lang))


@dp.message_handler(text='По должностям')
@dp.message_handler(text='By position')
async def form_position_set(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await Form.position.set()
        await message.answer(text=lang_message.get(lang).get('write_position'),
                             reply_markup=replyKeyboards.generator_cancel_keyboard(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(state=Form.position)
async def write_position(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        if message.text != lang_message.get(lang).get('cancel'):
            data['position'] += message.text.split(',')
            await state.finish()
            await message.answer(text=lang_message.get(lang).get('choose_category'),
                                 reply_markup=replyKeyboards.generator_filter_keyboards(lang))
        else:
            await state.finish()
            await message.answer(text=lang_message.get(lang).get('clicked_cancel'),
                                 reply_markup=replyKeyboards.generator_filter_keyboards(lang))


@dp.message_handler(text='По регионам')
@dp.message_handler(text='By region')
async def form_region_set(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await Form.region.set()
        await message.answer(text=lang_message.get(lang).get('write_region'),
                             reply_markup=replyKeyboards.generator_cancel_keyboard(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(state=Form.region)
async def write_region(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        if message.text != lang_message.get(lang).get('cancel'):
            data['region'] += message.text.split(',')
            await state.finish()
            await message.answer(text=lang_message.get(lang).get('choose_category'),
                                 reply_markup=replyKeyboards.generator_filter_keyboards(lang))
        else:
            await state.finish()
            await message.answer(text=lang_message.get(lang).get('clicked_cancel'),
                                 reply_markup=replyKeyboards.generator_filter_keyboards(lang))


@dp.message_handler(text='По отраслям')
@dp.message_handler(text='By industry')
async def form_industry_set(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await message.answer(text='...', reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(message.chat.id, message.message_id + 1)
        await message.answer(text=lang_message.get(lang).get('choose_industry'),
                             reply_markup=inlineKeyboards.generator_industry_inline_btn(lang, 1))
    else:
        await send_invoice_for_payment(message, lang)


@dp.callback_query_handler(text_contains="control")
async def change_page_of_industry_keyboard(call: CallbackQuery):
    await call.answer(cache_time=60)
    lang = db.get_user(call.message.chat.id)[5]
    industries = lang_message.get(lang).get('industries')
    status = call.data.split(':')[1]
    current_page = int(call.data.split(':')[2])
    if status == 'next':
        if not current_page == math.ceil(len(industries) / 10):
            current_page += 1
            await call.message.edit_reply_markup(reply_markup=
                                                 inlineKeyboards.generator_industry_inline_btn(lang, current_page))
    else:
        if not current_page == 1:
            current_page -= 1
            await call.message.edit_reply_markup(reply_markup=
                                                 inlineKeyboards.generator_industry_inline_btn(lang, current_page))


@dp.callback_query_handler(text_contains="industry")
async def change_page_of_industry_keyboard(call: CallbackQuery, state: FSMContext):
    lang = db.get_user(call.message.chat.id)[5]
    async with state.proxy() as data:
        index = call.data.split(":")[1]
        if index != "finish":
            elem = lang_message.get(lang).get('industries')[int(index)]
            industry_arr = data['industries']
            if not elem in industry_arr:
                industry_arr.append(elem)
            await call.message.delete()
            await call.message.answer(text=inlineKeyboards.generator_industry_message(lang, data['industries']),
                                      reply_markup=inlineKeyboards.generator_industry_inline_btn(lang, 1))
        else:
            await call.message.answer(text=lang_message.get(lang).get('choose_category'),
                                      reply_markup=replyKeyboards.generator_filter_keyboards(lang))


@dp.message_handler(text='Завершить')
@dp.message_handler(text='Finish')
async def form_message_set(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await Form.sms.set()

        await message.answer(text=lang_message.get(lang).get('write_message'), reply_markup=ReplyKeyboardRemove())
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(state=Form.sms)
async def save_message_to_data(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        data['sms'] = message.text
        await state.finish()
        if not db.exists_user_login(message.chat.id):
            await Form.login.set()
            await message.answer(text=lang_message.get(lang).get('write_login'))
        elif not db.exists_user_password(message.chat.id):
            data['login'] = db.get_user_info(message.chat.id)[0]
            await Form.password.set()
            await message.answer(text=lang_message.get(lang).get('write_password'))
        elif not db.exists_user_email(message.chat.id):
            data['login'] = db.get_user_info(message.chat.id)[0]
            data['password'] = db.get_user_info(message.chat.id)[1]
            await Form.email.set()
            await message.answer(text=lang_message.get(lang).get('write_email'))
        else:
            data['login'] = db.get_user_info(message.chat.id)[0]
            data['password'] = db.get_user_info(message.chat.id)[1]
            data['email'] = db.get_user_info(message.chat.id)[2]
            await message.answer(text=lang_message.get(lang).get('data_saved'),
                                 reply_markup=replyKeyboards.generator_last_keyboard(lang))


@dp.message_handler(state=Form.login)
async def enter_login(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        data['login'] = message.text
        db.update_login(message.chat.id, message.text)
        await state.finish()
        if not db.exists_user_password(message.chat.id):
            await Form.password.set()
            await message.answer(text=lang_message.get(lang).get('write_password'))
        elif not db.exists_user_email(message.chat.id):
            data['password'] = db.get_user_info(message.chat.id)[1]
            await Form.email.set()
            await message.answer(text=lang_message.get(lang).get('write_email'))
        else:
            data['password'] = db.get_user_info(message.chat.id)[1]
            data['email'] = db.get_user_info(message.chat.id)[2]
            await message.answer(text=lang_message.get(lang).get('data_saved'),
                                 reply_markup=replyKeyboards.generator_last_keyboard(lang))


@dp.message_handler(state=Form.password)
async def enter_pass(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        data['password'] = message.text
        db.update_password(message.chat.id, message.text)
        await state.finish()
        if not db.exists_user_email(message.chat.id):
            await Form.email.set()
            await message.answer(text=lang_message.get(lang).get('write_email'))
        else:
            data['email'] = db.get_user_info(message.chat.id)[2]
            await message.answer(text=lang_message.get(lang).get('data_saved'),
                                 reply_markup=replyKeyboards.generator_last_keyboard(lang))


@dp.message_handler(state=Form.email)
async def enter_email(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        data['email'] = message.text
        db.update_email(message.chat.id, message.text)
        await state.finish()
        await message.answer(text=lang_message.get(lang).get('data_saved'),
                             reply_markup=replyKeyboards.generator_last_keyboard(lang))


@dp.message_handler(text='Начать рассылку')
@dp.message_handler(text='Start mailing')
async def start_mailing(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        async with state.proxy() as data:
            data = data.as_dict()
            await send_email(data, message.chat.id, lang)
            await state.reset_data()
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(text='Поменять данные')
@dp.message_handler(text='Change data')
async def change_mailing(message: Message, state: FSMContext):
    await state.reset_data()
    await new_mailing(message, state)


@dp.message_handler(text='Отменить рассылку')
@dp.message_handler(text='Cancel mailing')
async def cancel_mailing(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await state.reset_data()
        await message.answer(text=lang_message.get(lang).get('cancel_action'),
                             reply_markup=replyKeyboards.generator_main_keyboards(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(Command('lang'))
@dp.message_handler(text='Изменить язык')
@dp.message_handler(text='Change language')
async def change_language(message: Message):
    lang = db.get_user(message.chat.id)[5]
    await Form.language.set()
    await message.answer(text=lang_message.get(lang).get('lang_change_text'),
                         reply_markup=replyKeyboards.lang_keyboard)


@dp.message_handler(state=Form.language)
async def update_language(message: Message, state: FSMContext):
    is_ru = message.text == '\U0001F1F7\U0001F1FA Русский'
    is_en = message.text == '\U0001F1EC\U0001F1E7 Engilsh'
    lang = 'ru'
    if is_ru:
        lang = 'ru'
    elif is_en:
        lang = 'eng'
    db.update_language(message.chat.id, lang)
    await state.finish()
    if db.is_paid(message.chat.id):
        await message.answer(text=lang_message.get(lang).get('lang_result_text'),
                             reply_markup=replyKeyboards.generator_main_keyboards(lang))
    else:
        await message.answer(text=lang_message.get(lang).get('lang_result_text'),
                             reply_markup=ReplyKeyboardRemove())
        await send_invoice_for_payment(message, lang)

    if not is_ru and not is_en:
        lang = db.get_user(message.chat.id)[5]
        await state.finish()
        await Form.language.set()
        await message.answer(text=lang_message.get(lang).get('lang_error'),
                             reply_markup=replyKeyboards.lang_keyboard)


def generator_account_message(lang, chat_id):
    msg_arr = lang_message.get(lang).get('your_account')
    user_info = db.get_user(chat_id)
    login = msg_arr[4]
    password = msg_arr[4]
    email = msg_arr[4]
    if user_info[2] is not None:
        login = user_info[2]
    if user_info[3] is not None:
        password = user_info[3]
    if user_info[4] is not None:
        email = user_info[4]

    msg_temp = msg_arr[0] + '\n' + msg_arr[1] + ': ' + login + '\n' \
               + msg_arr[2] + ': ' + password + '\n' + msg_arr[3] + ': ' + email

    return msg_temp


@dp.message_handler(Command('my_account'))
@dp.message_handler(text='Мой аккаунт')
@dp.message_handler(text='My account')
async def get_user_info(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        await message.answer(text=str(generator_account_message(lang, message.chat.id)),
                             reply_markup=replyKeyboards.generator_main_keyboards(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.message_handler(Command('edit_account'))
@dp.message_handler(text='Изменить логин/пароль/email')
@dp.message_handler(text='Change login/password/email')
async def change_data(message: Message):
    lang = db.get_user(message.chat.id)[5]
    if db.is_paid(message.chat.id):
        ques = lang_message.get(lang).get('choose_change_data')
        msg_temp = ques + '\n' + generator_account_message(lang, message.chat.id)
        await message.answer(text=msg_temp,
                             reply_markup=inlineKeyboards.generator_edit_account_keyboard(lang))
    else:
        await send_invoice_for_payment(message, lang)


@dp.callback_query_handler(text_contains='edit_account')
async def edit_account_callback(call: CallbackQuery, state: FSMContext):
    lang = db.get_user(call.message.chat.id)[5]
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        field = call.data.split(':')[1]
        if field == 'login':
            data['edit_account_field'] = 'login'
            await call.message.answer(text=lang_message.get(lang).get('write_login'))
        elif field == 'password':
            data['edit_account_field'] = 'password'
            await call.message.answer(text=lang_message.get(lang).get('write_password'))
        elif field == 'email':
            data['edit_account_field'] = 'email'
            await call.message.answer(text=lang_message.get(lang).get('write_email'))

        await Form.edit_account_field.set()


@dp.message_handler(state=Form.edit_account_field)
async def edit_account_field(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[5]
    async with state.proxy() as data:
        field = ''
        if data['edit_account_field'] == 'login':
            db.update_login(message.chat.id, message.text)
            field = lang_message.get(lang).get('your_account')[1]
        elif data['edit_account_field'] == 'password':
            db.update_password(message.chat.id, message.text)
            field = lang_message.get(lang).get('your_account')[2]
        elif data['edit_account_field'] == 'email':
            db.update_email(message.chat.id, message.text)
            field = lang_message.get(lang).get('your_account')[3]
        await state.finish()
        await message.answer(text=field + ' ' + lang_message.get(lang).get('account_edited'),
                             reply_markup=replyKeyboards.generator_main_keyboards(lang))
