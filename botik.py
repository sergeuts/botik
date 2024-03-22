from typing import Union, Any

import telebot  # pip install pyTelegramBotAPI https://pypi.org/project/pyTelegramBotAPI/
from telebot import types
import config

quest = config.quest
intros = config.intros
number_of_q = len(quest)

import urllib.request

bot = telebot.TeleBot(config.token)
user_state = {}
user_param = {'test_q_no': 0,
              'scores': [0, 0, 0, 0, 0, 0, 0, 0, 0],
              'results': [0, 0, 0, 0, 0, 0, 0, 0, 0],
              }

# test_q_no = 0
keybord_yes_no = 0
do_test = False

# @NSP_BAD_bot @NSP_BAD_1_bot

keybord_yes_no = types.InlineKeyboardMarkup(row_width=2)
yes_button = types.InlineKeyboardButton(text='Да', callback_data='yes')
no_button = types.InlineKeyboardButton(text='Нет', callback_data='no')
btn_menu = types.InlineKeyboardButton(text='Выход в главное меню', callback_data='menu')
keybord_yes_no.add(yes_button, no_button, btn_menu)

keybord_results = types.InlineKeyboardMarkup(row_width=2)
# btn_menu = types.InlineKeyboardButton(text='Выход в главное меню', callback_data='main_menu')
keybord_results.add(btn_menu)

keybord_main = types.InlineKeyboardMarkup(row_width=2)
yes_button = types.InlineKeyboardButton(text='Начать тест', callback_data='start_test')
no_button = types.InlineKeyboardButton(text='Описание теста', callback_data='test_info')
# btn_menu = types.InlineKeyboardButton(text='Выход в главное меню', callback_data='main_menu')
keybord_main.add(yes_button, no_button, btn_menu)

txt_menu = '''Список функций:'''
kbd_menu = types.InlineKeyboardMarkup(row_width=1)
btn_test_menu = types.InlineKeyboardButton(text='Пройти аналитический тест здоровья', callback_data='test_menu')
btn_bio_test_menu = types.InlineKeyboardButton(text='Биорезонансное тестирование', callback_data='bio_test_info')
btn_ask_question = types.InlineKeyboardButton(text='Задать вопрос', callback_data='ask_question')
btn_register = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='register')
btn_partner_programs = types.InlineKeyboardButton(text='Партнерские программы, заработок', callback_data='partner_programs')
btn_about_nsp = types.InlineKeyboardButton(text='О нашей компании и её продукции', callback_data='about_nsp')
btn_disc_card = types.InlineKeyboardButton(text='Получить дисконтную карту клиента', callback_data='get_disc_card')
# btn_menu = types.InlineKeyboardButton(text='Выход в главное меню', callback_data='get_disc_card')
kbd_menu.add(btn_test_menu, btn_bio_test_menu, btn_ask_question, btn_register, btn_partner_programs, btn_about_nsp, btn_disc_card)


# txt_welcome = '''Добро пожаловать!
# Вы общаетесь с чат ботом.
# <b>Управление и навигация по меню осуществляется с помощью зеленых кнопок внизу.</b>
# С помощью этого бота вы сможете:
# - Пройти аналитический тест здоровья ответив на 48 вопросов.
# - Узнать о нашей компании и её продукции.
# - Получить дисконтную карту клиента
# - Отправить нам свой вопрос или пожелание
# - Заказать обратный звонок специалиста для того чтобы:
#    - Получить бесплатную консультацию по оздоровительным программам.
#    - Записаться на обследование организма с помощью инновационной техники биорезонансного тестирования "Оберон".
#    - Узнать о проводимых вебинарах и лекциях оздоровительной тематики.
#    - Получить ответы на другие интересующие Вас вопросы.\n
# <b>Для прохождения теста нажмите кнопку "Начать тест".</b>'''

txt_welcome = '''Добро пожаловать!
<b>Для прохождения теста нажмите кнопку "Начать тест".</b>
<b>Управление и навигация по меню осуществляется с помощью кнопок внизу.</b>
'''


@bot.message_handler(content_types=["photo"])
def start1(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    ext = ''
    if len(file_info.file_path) > 4:
        if file_info.file_path[-4] == '.':
            ext = file_info.file_path[-4:]
    src = 'C:\\it\\Projects\\botik\\photos\\' + message.photo[-1].file_id[-4:] + ext
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, txt_welcome, parse_mode='html', reply_markup=keybord_main)



@bot.message_handler(commands=['menu'])
def start(message):
    bot.send_message(message.chat.id, txt_menu, parse_mode='html', reply_markup=kbd_menu)


    # bot.send_photo(message.chat.id, photo='https://drive.google.com/file/d/1RgvFCr4a6EQTSYGAFppyu-UwwJCVIQwL/view')
    # bot.send_sticker(message.chat.id, sticker='https://t.me/addstickers/HotCherry/4')
    # bot.send_sticker(message.chat.id, sticker='[ 😂 Sticker]')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global user_state
    if call.data in ['yes', 'no', 'start_test']:

        if call.data in ['yes', 'no']:
            if not call.from_user.username in user_state:
                user_state[call.from_user.username] = user_param.copy()
            q_no_prev: int = user_state[call.from_user.username]['test_q_no'] - 1
            if call.data == 'yes':
                scores = user_state[call.from_user.username]['scores']
                for s in range(len(scores)):
                    scores[s] += quest[q_no_prev][1][s] if call.data == 'yes' else 0
                user_state[call.from_user.username]['scores'] = scores
            if q_no_prev == number_of_q - 1:  # это последний вопрос
                scores = user_state[call.from_user.username]['scores']
                results = config.test(scores)
                user_state[call.from_user.username]['results'] = results
                user_state[call.from_user.username]['test_q_no'] = 0
                txt_results = '<b>Результаты теста:</b>\n'
                for r in range(len(results)):
                    bb, be = ('<b>', '</b>') if results[r] < 2 else ('', '')
                    txt_results += f'{config.systems[r][0]}:\n {bb}{config.marks[results[r]]}{be};\n\n'
                txt_results += '\nШкала оценок: Неудовлетворительно - Удовлетворительно - Хорошо - Очень хорошо.'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=txt_results, parse_mode='html', reply_markup=keybord_results)
                return
            else:
                user_state[call.from_user.username]['test_q_no'] += 1

        elif call.data == 'start_test':
            if not call.from_user.username in user_state:
                user_state[call.from_user.username] = user_param.copy()
            user_state[call.from_user.username]['test_q_no'] = 1
        q_no = user_state[call.from_user.username]['test_q_no'] - 1  # преобразование в индекс
        colon = ':' if quest[q_no][2] == 2 else ''
        msg = intros[quest[q_no][2]] + colon + ' <b>' + quest[q_no][0].lower() + '</b>?'
        msg = f'Отметьте те ощущения (симптомы), которые у Вас есть, ответив "да" или "нет". Вопрос {q_no + 1} из {number_of_q}:\n\n' + msg
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              parse_mode='html', reply_markup=keybord_yes_no)
    elif call.data == 'test_menu':
        # bot.send_message(message.chat.id, txt_welcome, parse_mode='html', reply_markup=keybord_main)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt_welcome,
                              parse_mode='html',
                              reply_markup=keybord_main)
    elif call.data == 'test_info':
        # info = '''Аналитический тест здоровья разработан лучшими специалистами-нутрициологами компании
        # <b>NSP - Nature’s Sunshine Products, Inc</b> - лидером на рынке Wellness (продукции для здоровья и красоты).'''
        info = '''Аналитический тест здоровья разработан специалистами-нутрициологами. 
        В тесте 48 вопросов, его можно пройти всего за 10 минут. Наш тест поможет своевременно выявить скрытые проблемы в работе Вашего организма, в отдельности по каждой системе. Вы сможете получите программу для восстановления здоровья, 
        включающую рекомендации по корректировке рациона питания и образа жизни! 
        Тест очень прост и в тоже время очень эффективен - Вам не нужно знать диагнозы или сдавать анализы. 
        Отметьте те ощущения (симптомы), которые у Вас есть, ответив "Да" или "Нет".
        <b>Предложите пройти этот тест своим друзьям в социальных сетях.</b>'''
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info,
                              parse_mode='html',
                              reply_markup=keybord_main)
    elif call.data == 'menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt_menu,
                              parse_mode='html',
                              reply_markup=kbd_menu)

@bot.message_handler(content_types=["text"])
def handle_txt(message):
    dev_chat_id = 1916153575
    if not message.from_user.username == 'serg_ut':
        mes = f'<b>{message.text}</b>\n from: {str(message.from_user.full_name)}, (ci:mi): ({str(message.chat.id)},{str(message.id)})'
        bot.send_message(dev_chat_id,  mes, parse_mode='html')
    else:
        if message.reply_to_message:
            pos = message.reply_to_message.text.find('ci:mi')
            if pos > -1:
                mes = message.reply_to_message.text[pos+9:-1]
                ci, mi = map(int, mes.split(','))
                bot.send_message(ci, message.text, parse_mode='html')

        #send_report()



# @bot.message_handler(content_types=["document"])
# def get_message(message):
#     main_keybord = types.InlineKeyboardMarkup(row_width=2)
#     yes_button = types.InlineKeyboardButton(text='Да', callback_data='yes')
#     no_button = types.InlineKeyboardButton(text='Нет', callback_data='no')
#     main_keybord.add(yes_button, no_button)
#     bot.send_message(message.chat.id, 'Вопросики', reply_markup=main_keybord)
#
#     global do_test
#     if do_test:
#         global cur_quest
#         cur_quest[message.chat.id] += 1
#         if cur_quest[message.chat.id] > 5:
#             do_test = False
#         bot.send_message(message.chat.id, quest[cur_quest[message.chat.id]][0], parse_mode='html')
#         button = types.ReplyKeyboardMarkup(row_width=2)  # resize_keyboard=True
#         btn1 = types.KeyboardButton('Да')
#         btn0 = types.KeyboardButton('Нет')
#         button.add(btn1, btn0)
#         bot.send_message(message.chat.id, 'Ваш ответ:', reply_markup=button)
    # if message.text == 'Помахай':
    #     # sticker = open('stickers/cherry_waves_her_hand.tgs', 'rb')
    #     # bot.send_sticker(message.chat.id, sticker)
    #     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANZYne8mAtOdt4uwjnkYRYqAxp2uxAAAgUAA8A2TxP5al-agmtNdSQE')
    # elif message.text == 'Похлопай':
    #     sticker = open('stickers/cherry_waves_her_hand.tgs', 'rb')
    #     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANUYne75L7rjavUkKSH1gAB2mq57BafAAIdAAPANk8TXtim3EE93kgkBA')
    #     # sticker.close()
    # elif message.text == 'Офис':
    #     bot.send_location(message.chat.id, 55.78306768925437, 37.59799936431071)
    # elif message.text == 'Menu 1':
    #     bot.send_message(message.chat.id, f'{message.text * 3}')


# @bot.message_handler(commands=['wave_hand'])
# def wave(message):
#     sticker = open('stickers/cherry_waves_her_hand.tgs', 'rb')
#     bot.send_sticker(message.chat.id, sticker)
#     sticker.close()


@bot.message_handler(content_types=["document"])
def handle_docs_audio(message):
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.token}/{file_info.file_path}', file_info.file_path)


# @bot.message_handler(content_types=["sticker"])
# def get_sticker(message):
#     #bot.send_message(message.chat.id, content_types, parse_mode='html')
#     sticker_id = message.sticker.file_id
#     bot.send_message(message.chat.id, f'sticker.file_id: {sticker_id}')
#
#     # file_info = bot.get_file(sticker_id)
#     # res = urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.token}/{file_info.file_path}', file_info.file_path)
#     # bot.send_sticker(message.chat.id, message.sticker.file_id)


# @bot.message_handler(commands=['menu'])
# def menu(message):
#     # button = types.InlineKeyboardMarkup()
#     # button.add(types.InlineKeyboardButton('Menu 1', url='ya.ru'))
#     # button.add(types.InlineKeyboardButton('Menu 2', url='ya.ru'))
#     bot.send_message(message.chat.id, 'msg', parse_mode='html')
#     button = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton('Menu_1', 'info')
#     btn2 = types.KeyboardButton('Menu_2')
#     button.add(btn1, btn2)
#     bot.send_message(message.chat.id, 'Ваш ответ:', reply_markup=button)

if __name__ == '__main__':
    # bot.polling(none_stop=True)
    bot.infinity_polling()
