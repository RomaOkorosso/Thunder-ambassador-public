import psycopg2
import telebot
from datetime import datetime
from config import connect_with_database


class User(object):

    def __init__(self, user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.city = city
        self.party = party
        self.hp = hp
        self.mp = mp
        self.force = force
        self.dmg = dmg
        self.defence = defence
        self.coin = coin
        self.donate_coin = donate_coin

    def make_me_msg(self):
        stats = [self.user_id, self.username, self.name, self.city, self.party, self.hp, self.mp, self.force, self.dmg,
                 self.defence, self.coin, self.donate_coin]
        icons = ['ID:', 'Юзернейм:', "Имя:", 'Город:', '👨‍👨‍👧‍👦 Отряд:', '❤️ Хп:', '🔮 Мана:', '💪 Сила:',
                 '⚔️ Урон:',
                 '🛡 Защита:', '💰 Монеты:', '🧧 Обои:']
        return '\n'.join((f'{icon} {stat}' for icon, stat in zip(icons, stats))) + f'\n🥊 БМ: {self.hp + self.force}'


def create_db():
    try:
        con = connect_with_database()
        cur = con.cursor()
        cur.execute(f"""DELETE FROM profiles WHERE user_id = 374085219""")
        con.commit()
        con.close()
    except Exception as error:
        print(error)


def get_update_interval(user_id):
    try:
        con = connect_with_database()
        cur = con.cursor()
        cur.execute(f"""SELECT last_update_time FROM profiles WHERE user_id = {user_id}""")
        db = cur.fetchone()
        cur.execute("""SELECT now()::timestamp""")
        last_date = datetime(db[0].year, db[0].month, db[0].day, db[0].hour, db[0].minute, db[0].second)
        now = cur.fetchone()
        now_time = datetime(now[0].year, now[0].month, now[0].day, now[0].hour, now[0].minute, now[0].second)
        con.close()
        interval = (now_time - last_date)
        sec = interval.seconds
        hour = sec // 3600
        sec -= hour * 3600
        mins = sec // 60
        sec -= mins * 60
        if hour in [1, 21]:
            hour_name_ru = 'час'
        elif hour in [2, 3, 4, 22, 23, 24]:
            hour_name_ru = 'часа'
        else:
            hour_name_ru = 'часов'
        if mins in [1, 21, 31, 41, 51]:
            mins_name_ru = 'минута'
        elif mins in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            mins_name_ru = 'минуты'
        else:
            mins_name_ru = 'минут'
        icon = ["дней ", f"{hour_name_ru} ", f"{mins_name_ru} ", "секунд "]
        a = [interval.days, hour, mins, sec]
        new_interval = '\nС последнего обновления прошло:\n'
        for i in range(len(a)):
            if a[i] != 0:
                new_interval += f'{a[i]} {icon[i]}'
        return new_interval
    except Exception as error:
        print(error)


def save_profile(user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin):
    con = connect_with_database()
    cur = con.cursor()
    cur.execute(f"""SELECT user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin, 
                    last_update_time FROM profiles WHERE user_id = {user_id}""")
    db = cur.fetchone()
    msg = ''
    if db is None:
        cur.execute(f"""INSERT INTO profiles (user_id, username, name, city, party, hp, mp, force, dmg, defence, coin,
                        donate_coin, last_update_time) 
                        VALUES ({user_id},'{username}', '{name}', '{city}', '{party}', {hp}, {mp}, {force}, {dmg}, 
                        {defence}, {coin}, {donate_coin}, now())""")
        msg += f"Профиль сохранен в межгородском реестре!\nХорошой игры, <a href='tg://user?id={user_id}'>{name}</a>!"
        con.commit()
        con.close()
        return msg
    else:
        txt_stats = 'user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin'.split(', ')
        new_stats = [user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin]
        icons = ['ID:', 'Юзернейм:', "Имя:", 'Город:', '👨‍👨‍👧‍👦:', '❤️:', '🔮:', '💪:', '⚔️:', '🛡:', '💰:', '🧧:']
        msg += f"<a href='tg://user?id={user_id}'>{name}</a>, реестр города вскоре получит твои новые данные"
        updt = ''
        for i in range(len(new_stats)):
            if i in [0, 5, 6, 7, 8, 9, 10, 11]:
                if int(new_stats[i]) != int(db[i]):
                    if int(db[i]) < int(new_stats[i]):
                        msg += f"\n{icons[i]} +{int(new_stats[i]) - int(db[i])}"
                    else:
                        msg += f"\n{icons[i]} -{int(db[i]) - int(new_stats[i])}"
                    updt += f"{txt_stats[i]} = {new_stats[i]}, "
            elif i not in [0, 5, 6, 7, 8, 9] and new_stats[i] != db[i]:
                msg += f"\n{icons[i]} {new_stats[i]}"
                updt += f"{txt_stats[i]} = '{new_stats[i]}', "
        updt += 'last_update_time = now()'
        msg += get_update_interval(user_id)
        cur.execute(f"""UPDATE profiles SET {updt} WHERE user_id = {user_id}""")
        con.commit()
        con.close()
        return msg


def get_user_info(user_id):
    con = connect_with_database()
    cur = con.cursor()
    cur.execute(f"""SELECT user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin
                     FROM profiles WHERE user_id = {user_id}""")
    db = cur.fetchone()
    con.close()
    if db is not None:
        user = User(*db)
        # user_id, username, name, city, party, hp, mp, force, dmg, defence, coin, donate_coin = db
        msg = f"<a href='tg://user?id={user_id}'>{user.name}</a>, реестр города сообщает о тебе это:\n"
        msg += user.make_me_msg()
        msg += get_update_interval(user_id)

    else:
        msg = 'Реестр города не отзывается, покажи мне свой профиль для начала!'
    return msg


def get_squad(squad_name):
    con = connect_with_database()
    cur = con.cursor()
    cur.execute(f"""SELECT username, name, user_id, hp, force, last_update_time FROM profiles WHERE party 
    LIKE '{squad_name}'""")
    db = cur.fetchall()
    con.close()
    msg = ''
    for i in range(len(db)):
        msg += f'<a href="tg://user?id={db[i][2]}">{db[i][1]}</a>, БМ: {db[i][3] + db[i][4]},' \
            f' {get_update_interval(db[i][2])}\n\n'
    return msg
