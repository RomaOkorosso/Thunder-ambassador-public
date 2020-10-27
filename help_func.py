import datetime
import pytz


def get_now_time() -> str:
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    now_time = now.strftime("%H:%M")
    return now_time


def hero_parser(txt):
    left = txt.find('👤 ') + len('👤 ')
    name = txt[left:txt.find(',', left)]
    left = txt.find(', ', left) + len(', ')
    city = txt[left:txt.find('\n', left)]
    left = txt.find('\n👨‍👨‍👧‍👦: ', left) + len('\n👨‍👨‍👧‍👦: ')
    party = txt[left:txt.find('\n', left)]
    left = txt.find('❤️: ') + len('❤️: ')
    right = txt.find(' | ', left)
    hp = txt[txt.find('/', left) + 1:right]
    left = right + len(' | 🔮: ')
    right = txt.find('\n', left)
    left = txt.find('/', left)
    mp = txt[left + 1:right]
    left = right + len('\n💪: ')
    right = txt.find(' | ', left)
    force = txt[left:right]
    left = right + len(' | ⚔️: ')
    right = txt.find(' | ', left)
    dmg = txt[left:right]
    left = right + len(' | 🛡: ')
    right = txt.find('\n', left)
    defence = txt[left:right]
    left = txt.find('💰: ', left) + len('💰: ')
    right = txt.find(', 🧧: ')
    coin = txt[left:right]
    left = right + len(', 🧧: ')
    right = txt.find('\n', left)
    donate_coin = txt[left:right]
    return name, city, party, hp, mp, force, dmg, defence, coin, donate_coin


def get_time_to_raid() -> str:
    try:
        now_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        deltas = []
        raid_time = [datetime.datetime(1, 1, 1, hour=21, minute=0, second=00, microsecond=0, tzinfo=pytz.utc),
                     datetime.datetime(1, 1, 1, hour=13, minute=0, second=00, microsecond=0, tzinfo=pytz.utc),
                     datetime.datetime(1, 1, 1, hour=5, minute=0, second=00, microsecond=0, tzinfo=pytz.utc)]
        for i in raid_time:
            delta = i - now_time
            sec = delta.seconds
            hour = sec // 3600
            sec -= hour * 3600
            mins = sec // 60
            sec -= mins * 60
            deltas.append([hour, mins, sec])
            # print(f"{hour}:{mins}:{sec}")
        deltas.sort()
        if deltas[0][0] in [1, 21]:
            hour_name_ru = 'час'
        elif deltas[0][0] in [2, 3, 4, 22, 23, 24]:
            hour_name_ru = 'часа'
        else:
            hour_name_ru = 'часов'
        if deltas[0][1] in [1, 21, 31, 41, 51]:
            mins_name_ru = 'минута'
        elif deltas[0][1] in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            mins_name_ru = 'минуты'
        else:
            mins_name_ru = 'минут'
        msg_txt = f"<code>До ближайшего рейда осталось: {deltas[0][0]} {hour_name_ru}\
         {deltas[0][1]} {mins_name_ru} < / code > "
        return msg_txt
    except:
        return "Случились технические шоколадки, приношу свои изенения🙈"
