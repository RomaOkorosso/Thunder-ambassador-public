import telebot
import config
import database_functions
import help_func
from telebot import types

roman = config.roman
bot = telebot.TeleBot(config.main)
bot.send_message(roman, f'bot started at {help_func.get_now_time()}')
game_bot = 820567103

locations_to_find = ['⛏ Шахта Кобольдов', '👹Пещера Троллей', '👨‍🎤Воровской притон', '🧜‍♀Бухта русалок',
                     '🏰Замок "Голубая Кровь"', '🧟‍♂Заброшенная тюрьма', '🎪Оргриммар', '🏰Хогвартс',
                     '🌒Темная сторона',
                     '🌳 Лесопилка', '⛏ Рудная шахта', '🏜 Карьер', '✨ Магическая поляна', '🗿 Плато демонов',
                     '🏤 Ломбард', '🏚 Прием металлолома', '🌴 Пальмовая роща']


def make_log(message):
    log = f'<code>{message.chat.id}\n{message.chat.title}\n{message.from_user.id} @ {message.from_user.username}\n' \
        f'</code>"{message.text}"\n{help_func.get_now_time()}'
    return log


@bot.message_handler(commands=['start', 'help', 'me', 'time', 'db', 'raid_time', 'donate', 'make_pin', 'check_squad',
                               'edit_coord'])
def main_commands(message):
    try:
        chat_id = message.chat.id
        msg = str(message.text)
        bot.send_message('-1001235101505', make_log(message), parse_mode='HTML')
        if msg == '/start' or msg == '/start@@ThunderAmbassadorBot':
            bot.send_message(chat_id, 'Привет, я вижу скорую бурю, позволь мне помочь тебе?')
        elif msg == '/help' or msg == '/help@ThunderAmbassadorBot':
            bot.send_message(chat_id, 'Если ты не понимаешь как мной пользоваться, я дам тебе подсказку //ссылка//')
        elif msg == '/me' or msg == '/me@ThunderAmbassadorBot':
            msg = database_functions.get_user_info(message.from_user.id)
            bot.send_message(chat_id, msg, parse_mode="HTML")
        elif msg == '/db' and message.from_user.id == roman:
            database_functions.create_db()
        elif '/raid_time' == msg or '/raid_time@ThunderAmbassadorBot' == msg:
            bot.send_message(chat_id, help_func.get_time_to_raid(), parse_mode="HTML")
        elif '/donate' in msg:
            usr = message.from_user.id
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton('ЯндексДенюшки', url=f'https://money.yandex.ru/to/410019603804361?comment='
            f'Пожертвование на развите бота от {usr}')
            markup.add(btn)
            bot.send_message(message.chat.id,
                             f'<b>Поддержать штаны и избавить от голодной смерти разработчика можно по этим'
                             f' ссылкам:\nИли напишите в лс, если другой способ предпочтительнее</b>',
                             parse_mode='HTML', disable_notification=True, disable_web_page_preview=True,
                             reply_markup=markup)
        elif '/time' == msg or '/time@ThunderAmbassadorBot' == msg:
            bot.send_message(chat_id, f"Сейчас {help_func.get_now_time()} по UTC +0000")
        elif '/make_pin' in msg and message.from_user.id in [roman, 479807824, 381843491]:
            pin_txt = msg[msg.find('/make_pin')::]
            # pin_id = bot.send_message()
        elif '/check_squad' in msg and message.from_user.id in [roman, 479807824, 381843491]:
            squad_name = msg[msg.find(' ') + 1:]
            msg_txt = str(database_functions.get_squad(squad_name))
            if len(msg_txt) > 34000:
                while len(msg_txt) > 34000:
                    right = msg_txt.find('\n', 34000)
                    sep = msg_txt[0:right]
                    msg_txt = msg_txt[right:]
                    bot.send_message(message.chat.id, sep, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, msg_txt, parse_mode='HTML')



    except Exception as err:
        err = str(err) + f'\n at {message.chat.id}\n{message.chat.title}'
        bot.send_message(roman, err)


@bot.message_handler(content_types=['text'])
def send_msg(message):
    try:
        bot.send_message('-1001235101505', make_log(message), parse_mode='HTML')
        chat_id = message.chat.id
        msg = str(message.text)
        if 'UID: ' in msg and 'Событие:' in msg and '👤' in msg and message.forward_from is not None:
            if message.forward_from.id == game_bot and (message.date - 60 * 5 <= message.forward_date or
                                                        message.from_user.id == roman):
                user_id = str(message.from_user.id)
                check_id = msg[msg.find('UID: ') + len('UID: '):]
                if user_id == check_id:
                    update_info = database_functions.save_profile(user_id, message.from_user.username,
                                                                  *help_func.hero_parser(msg))
                    bot.send_message(message.chat.id, update_info, parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Мне жизненно необходим именно твой профиль')

    except Exception as err:
        err = str(err) + f'\n at {message.chat.id}\n{message.chat.title}'
        bot.send_message(roman, err)


bot.polling(none_stop=True)
