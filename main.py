import emoji
import sqlite3
import telebot
from telebot import types
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import date

bot = telebot.TeleBot('')
chat1 = 123456789
chat_chat = 'secret'
chat_m = None
chat_id12 = 1
chat_id13 = 1
second_id = None
msgID = None
msgID_second = None

name = None
admin = None

# Google sheets
gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gcredentials = 'bot-telegram-392510-06cbc02d241e.json'
gdocument = 'Table'

user_dict = {}
user_chat_dict = {}
users_dict = {}

user_name = None


class User:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.master = None
        self.admin = None
        self.administr = None


class Userchat:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.master = None
        self.admin = None
        self.administr = None


class Userchat_forclose:
    def __init__(self, name):
        self.name = name
        self.surname = None
        self.master = None
        self.admin = None
        self.administr = None


app_dict = {}

city = None
equipment = None
damage = None
number = None
surname = None
status = None
master = None
master_surname = None
message = None
percent = None
administr = None
comment = None


class App:
    def __init__(self, city):
        self.city = city
        self.equipment = None
        self.damage = None
        self.number = None
        self.name = None
        self.surname = None
        self.status = None
        self.master = None
        self.master_surname = None
        self.nomer = None
        self.message = None
        self.dataapp = None
        self.msgadm = None
        self.msgmaster = None
        self.comment = None


# start command, create a database and suggest who to register with
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('users.sql')
    conn_chat = sqlite3.connect('users_chat.sql')
    conn_app = sqlite3.connect('app.sql')
    conn_close = sqlite3.connect('closes.sql')
    cur = conn.cursor()
    cur_close = conn_close.cursor()
    cur_chat = conn_chat.cursor()
    cur_app = conn_app.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id integer primary key, name varchar(50), surname varchar(50),'
        'master varchar(50),admin varchar(50), administr varchar(50) )')
    cur_chat.execute(
        'CREATE TABLE IF NOT EXISTS users_chat (id integer, name varchar(50), surname varchar(50),master varchar(50),'
        'admin varchar(50), administr varchar(50) )')
    cur_app.execute(
        'CREATE TABLE IF NOT EXISTS app (id integer primary key, dataapp varchar(50), city varchar(50), equipment '
        'varchar(50), damage varchar(50), number varchar(50), name varchar(50), surname varchar(50), status varchar('
        '50),master varchar(50), master_surname varchar(50), nomer varchar(50), message int,msgadm int,msgmaster int, '
        'comment varchar(50))')
    cur_close.execute(
        'CREATE TABLE IF NOT EXISTS closes (id integer, name varchar(50), surname varchar(50),master varchar(50),'
        'admin varchar(50), administr varchar(50) )')
    conn.commit()
    conn_app.commit()
    conn_chat.commit()
    cur_app.close()
    cur.close()
    cur_chat.close()
    conn.close()
    conn_app.close()
    conn_chat.close()
    db_users_chat()
    if message.chat.id in user_chat_dict.keys():
        user = user_chat_dict[message.chat.id]
        if user.master == "yes" or user.admin == "yes":
            bot.send_message(message.chat.id, "Вы уже зарегистрированы")
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_admin = types.InlineKeyboardButton(text='Админ', callback_data='admin')
        keyboard.add(key_admin)
        key_master = types.InlineKeyboardButton(text='Мастер', callback_data='master')
        keyboard.add(key_master)
        key_administ = types.InlineKeyboardButton(text='Администрация', callback_data='administr')
        keyboard.add(key_administ)
        question = 'Здравствуйте! Выберите кем вы являетесь'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    if message.chat.id == chat_chat:
        bot.delete_message(message.chat.id, message.id)


def db_users_close():
    conn = sqlite3.connect('closes.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM closes')
    num = cur.fetchall()
    for el in num:
        user_number = el[0]
        user = Userchat_forclose(name)
        users_dict[user_number] = user
        cur.execute('SELECT * FROM closes where id = ?', (el[0],))
        num = cur.fetchall()
        for element in num:
            user.name = element[1]
            user.surname = element[2]
            user.admin = element[4]
            user.master = element[3]
            user.administr = element[5]
    conn.commit()
    cur.close()
    conn.close()


def db_users_chat():
    conn = sqlite3.connect('users_chat.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users_chat')
    num = cur.fetchall()
    for el in num:
        user_number = el[0]
        user = Userchat(name)
        user_chat_dict[user_number] = user
        cur.execute('SELECT * FROM users_chat where id = ?', (el[0],))
        num = cur.fetchall()
        for element in num:
            user.name = element[1]
            user.surname = element[2]
            user.admin = element[4]
            user.master = element[3]
            user.administr = element[5]
    conn.commit()
    cur.close()
    conn.close()


def db_users():
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM USERS')
    num = cur.fetchall()
    for el in num:
        user_number = el[0]
        user = User(name)
        user_dict[user_number] = user
        cur.execute('SELECT * FROM USERS where id = ?', (el[0],))
        num = cur.fetchall()
        for element in num:
            user.name = element[1]
            user.surname = element[2]
            user.admin = element[4]
            user.master = element[3]
            user.administr = element[5]
    conn.commit()
    cur.close()
    conn.close()


def db_app():
    conn_app = sqlite3.connect('app.sql')
    cur = conn_app.cursor()
    cur.execute('SELECT * FROM app')
    num = cur.fetchall()
    for el in num:
        app_number = el[0]
        app = App(city)
        app_dict[app_number] = app
        cur.execute('SELECT * FROM app where id = ?', (el[0],))
        num = cur.fetchall()
        for element in num:
            app.dataapp = element[1]
            app.city = element[2]
            app.equipment = element[3]
            app.damage = element[4]
            app.number = element[5]
            app.name = element[6]
            app.surname = element[7]
            app.status = element[8]
            app.master = element[9]
            app.master_surname = element[10]
            app.nomer = element[0]
            app.message = element[12]
            app.msgadm = element[13]
            app.msgmaster = element[14]
            app.comment = element[15]
    conn_app.commit()
    cur.close()
    conn_app.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global chat1, chat_m, msgID, second_id, percent, msgID_second, text_table
    if call.data == "admin" or call.data == "master":
        db_users_chat()
        if call.message.chat.id in user_chat_dict.keys():
            user = user_chat_dict[call.message.chat.id]
            if user.master == "yes" or user.admin == "yes":
                bot.send_message(call.message.chat.id, "Вы уже зарегистрированы")
        else:
            question = 'Введите имя'
            msg = bot.send_message(call.message.chat.id, text=question)
            if call.data == "admin":
                bot.register_next_step_handler(msg, process_name_step)
            elif call.data == "master":
                bot.register_next_step_handler(msg, process_name_master_step)
    # check if the user is in the administration, if at least once yes, then write about it
    elif call.data == "administr":
        db_users()
        flag = 0
        for i in range(1, len(user_dict) + 1):
            user = user_dict[int(i)]
            if user.administr is not None:
                flag = user.surname
                break
        if flag != 0:
            if call.message.chat.id in user_chat_dict.keys():
                user = user_chat_dict[call.message.chat.id]
                if user.surname == flag:
                    question = 'Вы уже верифицированы, повторная верификация не требуется'
                    bot.send_message(call.message.chat.id, text=question)
            else:
                question = 'Администрация прошла верификацию, вы не можете использовать эту роль'
                bot.send_message(call.message.chat.id, text=question)
        else:
            question = 'Введите пароль'
            msg = bot.send_message(call.message.chat.id, text=question)
            bot.register_next_step_handler(msg, process_password)
    # the administration either approves the new admin or they don't
    elif "take" in call.data:
        bot.send_message(call.message.chat.id,
                         text=call.data.partition('take')[0] + " назначен админом")
        bot.send_message(int(call.data[call.data.find("take") + 4:]),
                         text="Вы успешно зарегистрированы админом")
        bot.edit_message_text(call.data.partition('take')[0] + " регистрируется под админа", call.message.chat.id,
                              call.message.id, reply_markup=None)
    elif "dont" in call.data:
        conn_app = sqlite3.connect('users.sql')
        cur = conn_app.cursor()
        conn2_app = sqlite3.connect('users_chat.sql')
        cur2 = conn2_app.cursor()
        conn3_app = sqlite3.connect('closes.sql')
        cur3 = conn3_app.cursor()
        cur.execute(
            "DELETE FROM users WHERE master = ?",
            ("delete",)
        )
        cur2.execute(
            "DELETE FROM users_chat WHERE master = ?",
            ("delete",)
        )
        cur3.execute(
            "DELETE FROM closes WHERE master = ?",
            ("delete",)
        )
        conn_app.commit()
        cur.close()
        conn_app.close()
        conn2_app.commit()
        cur2.close()
        conn2_app.close()
        conn3_app.commit()
        cur3.close()
        conn3_app.close()
        bot.send_message(int(call.data[call.data.find("dont") + 4:]),
                         "Заявка на админа отклонена, выберите роль мастера")
    elif call.data == "yes":
        try:
            db_users_chat()
            userchat = user_chat_dict[int(call.message.chat.id)]
            if userchat.admin == "yes":
                question = 'Введите город'
                msg = bot.send_message(call.message.chat.id, text=question)
                bot.register_next_step_handler(msg, process_city_step)
            else:
                bot.send_message(call.message.chat.id, text="Вы являетесь мастером и не можете оставлять заявки")
        except Exception:
            bot.send_message(call.message.chat.id, text="Необходимо зарегистрироваться")
    elif "close" in call.data:
        try:
            db_users_close()
            userclose = users_dict[int(call.from_user.id)]
            if userclose.admin == "yes":
                db_app()
                conn_app = sqlite3.connect('app.sql')
                cur = conn_app.cursor()
                cur.execute(
                    "UPDATE app SET status = ? WHERE id = ?",
                    ("закрыта", int(call.data[call.data.find("close") + 5:]))
                )
                conn_app.commit()
                cur.close()
                conn_app.close()
                db_app()
                app = app_dict[int(call.data[call.data.find("close") + 5:])]
                bot.delete_message(chat_id=chat_chat, message_id=call.message.id)
                delete_from_sheet(int(app.nomer))
                add_to_gsheet(call.message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage,
                              app.comment,
                              app.number,
                              app.name,
                              None, "закрыто администратором", None, None, None)
            else:
                bot.send_message(call.from_user.id, text="Мастер не может удалять заявки")
        except Exception:
            return
    elif "diagn" in call.data:
        try:
            db_app()
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET status = ? WHERE id = ?",
                ("закрыта, диагностика", int(call.data[call.data.find("diagn") + 5:]))
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            db_app()
            app = app_dict[int(call.data[call.data.find("diagn") + 5:])]
            app.status = "закрыта, диагностика"
            text = "Опишите результаты диагностики"
            second_id = int(call.data[call.data.find("diagn") + 5:])
            msgID = call.data.partition('diagn')[0]
            msgID_second = int(call.message.id)
            msg = bot.send_message(chat_id=call.message.chat.id, text=text)
            bot.register_next_step_handler(msg, process_diagn)
        except Exception:
            return
    elif "complete" in call.data:
        try:
            db_app()
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET status = ? WHERE id = ?",
                ("закрыта, ремонт выполнен", int(call.data[call.data.find("complete") + 8:]))
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            db_app()
            app = app_dict[int(call.data[call.data.find("complete") + 8:])]
            app1 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, ремонт выполнен' + ' (' + app.master + " " + app.master_surname + ") "
            app2 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, ремонт выполнен' + ' (' + app.master + " " + app.master_surname + ")"
            bot.edit_message_text(chat_id=chat_chat, message_id=call.data.partition('complete')[0], text=app1,
                                  parse_mode="html")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=app2,
                                  parse_mode="html", reply_markup=None)
            keyboard1 = types.InlineKeyboardMarkup()
            key_yes = types.InlineKeyboardButton(text='% отправлен',
                                                 callback_data='send' + call.data[call.data.find("complete") + 8:])
            keyboard1.add(key_yes)
            text = "Опишите выполнение работы"
            second_id = int(call.data[call.data.find("complete") + 8:])
            msgID = int(call.message.id)
            msg = bot.send_message(chat_id=call.message.chat.id, text=text)
            bot.register_next_step_handler(msg, process_complete)
        except Exception:
            return

    elif "newmaster" in call.data:
        text = "Напишите комментарий, почему нужен другой мастер:"
        msg = bot.send_message(chat_id=call.message.chat.id, text=text)
        second_id = call.data.partition('newmaster')[0]
        msgID = int(call.data[call.data.find("newmaster") + 9:])
        msgID_second = int(call.message.id)
        bot.register_next_step_handler(msg, process_newmaster)

    elif "client" in call.data:
        try:
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET status = ? WHERE id = ?",
                ("клиент отменил заявку", int(call.data[call.data.find("client") + 6:]))
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            db_app()
            app = app_dict[int(call.data[call.data.find("client") + 6:])]
            app1 = emoji.emojize(":black_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nСтатус: клиент отменил заявку '
            app2 = emoji.emojize(":black_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + '\nСтатус: клиент отменил заявку '
            bot.edit_message_text(chat_id=chat_chat, message_id=call.data.partition('client')[0], text=app1,
                                  parse_mode="html")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=app2,
                                  parse_mode="html")
            delete_from_sheet(int(app.nomer))
            add_to_gsheet(call.message.chat.id, app.nomer, app.dataapp, app.city, app.equipment,
                          app.damage, app.comment, app.number,
                          app.name,
                          str(app.master + " " + app.master_surname), "клиент отменил заявку", None, None, None)
        except Exception:
            return

    elif "accept" in call.data:
        try:
            n_dict = int(call.data[call.data.find("accept") + 6:])
            db_app()
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET status = ? WHERE id = ?",
                ("договорился", n_dict)
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            db_app()
            app = app_dict[n_dict]

            keyboard1 = types.InlineKeyboardMarkup()
            key_yes = types.InlineKeyboardButton(text='Диагностика',
                                                 callback_data=call.data.partition('accept')[0] + 'diagn' + str(n_dict))
            keyboard1.add(key_yes)
            key_no = types.InlineKeyboardButton(text='Ремонт выполнен',
                                                callback_data=call.data.partition('accept')[0] + 'complete' + str(
                                                    n_dict))
            keyboard1.add(key_no)
            key_client = types.InlineKeyboardButton(text='Клиент отменил заявку',
                                                    callback_data=call.data.partition('accept')[0] + 'client' + str(
                                                        n_dict))
            keyboard1.add(key_client)
            app1 = emoji.emojize(":blue_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nКомментарий: ' + app.comment + '\nСтатус: договорился ' + app.master + " " + app.master_surname
            app2 = emoji.emojize(":blue_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + '\nКомментарий: ' + app.comment + '\nСтатус: договорился ' + app.master + " " + app.master_surname
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=app2,
                                  reply_markup=keyboard1, parse_mode="html")
            bot.edit_message_text(chat_id=chat_chat, message_id=call.data.partition('accept')[0], text=app1,
                                  parse_mode="html")
            try:
                delete_from_sheet(int(app.nomer))
                add_to_gsheet(call.message.chat.id, app.nomer, app.dataapp, app.city, app.equipment,
                              app.damage, app.comment, app.number,
                              app.name,
                              str(app.master + " " + app.master_surname), "в работе", None, None, None)
            except Exception:
                return
        except Exception:
            return
    elif "noacc" in call.data:
        try:
            db_app()
            second_id = call.data.partition('noacc')[0]
            msgID = int(call.data[call.data.find("noacc") + 5:])
            app = app_dict[int(call.data[call.data.find("noacc") + 5:])]
            text = "Напишите кратко комментарий"
            msg = bot.send_message(chat_id=call.message.chat.id, text=text)
            delete_from_sheet(int(app.nomer))
            bot.register_next_step_handler(msg, process_no_accept)
        except Exception:
            return

    elif "send" in call.data:
        try:
            db_app()
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET msgmaster = ? WHERE id = ?",
                (int(call.message.chat.id), int(call.data[call.data.find("send") + 4:]))
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            db_app()
            app = app_dict[int(call.data[call.data.find("send") + 4:])]
            textadm = "По заявке № " + str(
                app.nomer) + " мастер " + app.master + " " + app.master_surname + " отправил процент в размере " + str(
                percent) + ",подтверждаете?"
            keyboard1 = types.InlineKeyboardMarkup()
            key_no = types.InlineKeyboardButton(text='Подтверждаю',
                                                callback_data='agree' + str(call.data[call.data.find("send") + 4:]))
            keyboard1.add(key_no)
            msgID = int(call.data[call.data.find("send") + 4:])
            app2 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + "\nКомментарий: " + app.comment + '\nСтатус: администратор подтверждает перевод'
            bot.send_message(int(app.msgadm), textadm, reply_markup=keyboard1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=app2,
                                  parse_mode="html", reply_markup=None)
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET msgadm = ? WHERE id = ?",
                (int(call.message.id), int(call.data[call.data.find("send") + 4:]))
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            text1 = str(percent)
            text2 = "закрыта ремонтом"
            text3 = "процент переведен" + " " + str(date.today())
            delete_from_sheet(int(app.nomer))
            add_to_gsheet(call.message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage,
                          app.comment,
                          app.number,
                          app.name,
                          str(app.master + " " + app.master_surname), text2, text1, text3, None)
        except Exception:
            return

    elif "agree" in call.data:
        try:
            text1 = "закрыта ремонтом" + str(text_table)
            text2 = str(percent)
            text3 = "процент переведен" + " " + str(date.today())
            text4 = "Подтверждено"
            db_app()
            conn_app = sqlite3.connect('app.sql')
            cur = conn_app.cursor()
            cur.execute(
                "UPDATE app SET status = ? WHERE id = ?",
                ("закрыта, отчитана", int(call.data[call.data.find("agree") + 5:]))
            )
            conn_app.commit()
            cur.close()
            conn_app.close()
            db_app()
            app = app_dict[int(call.data[call.data.find("agree") + 5:])]
            app.status = "закрыта, отчитана"
            textadmin = "Заявка № " + str(app.nomer) + " закрыта"
            textadm = "По заявке № " + str(
                app.nomer) + " мастер" + app.master + " " + app.master_surname + " отправил процент в размере " + str(
                percent) + ",подтверждаете?"
            text = "Администратор подтвердил перевод по заявке № " + str(app.nomer) + " ,заявка закрыта"
            app2 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, отчитана'
            bot.send_message(call.message.chat.id, textadmin)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=textadm,
                                  reply_markup=None)
            bot.edit_message_text(chat_id=int(app.msgmaster), message_id=int(app.msgadm), text=app2,
                                  parse_mode="html", reply_markup=None)
            bot.send_message(int(app.msgmaster), text)
            delete_from_sheet(int(app.nomer))
            add_to_gsheet(call.message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage,
                          app.comment,
                          app.number, app.name,
                          str(app.master + " " + app.master_surname), text1, text2, text3, text4)
        except Exception:
            return

    else:
        try:
            db_users_chat()
            userchat = user_chat_dict[int(call.from_user.id)]
            if userchat.admin == "yes":
                bot.send_message(call.from_user.id, "Администратор может только оставлять заявки")
            else:
                conn_app = sqlite3.connect('app.sql')
                cur = conn_app.cursor()
                db_app()
                db_users_chat()
                user = user_chat_dict[int(call.from_user.id)]
                cur.execute(
                    "UPDATE app SET status = ? WHERE id = ?",
                    ("договаривается", int(call.data))
                )
                cur.execute(
                    "UPDATE app SET master = ? WHERE id = ?",
                    (user.name, int(call.data))
                )
                cur.execute(
                    "UPDATE app SET master_surname = ? WHERE id = ?",
                    (user.surname, int(call.data))
                )
                conn_app.commit()
                cur.close()
                conn_app.close()
                db_app()
                app = app_dict[int(call.data)]
                keyboard1 = types.InlineKeyboardMarkup()
                key_yes = types.InlineKeyboardButton(text='Договорился',
                                                     callback_data=str(call.message.id) + 'accept' + call.data)
                keyboard1.add(key_yes)
                key_no = types.InlineKeyboardButton(text='Не договорился',
                                                    callback_data=str(call.message.id) + 'noacc' + call.data)
                keyboard1.add(key_no)
                key_master = types.InlineKeyboardButton(text='Нужен другой мастер',
                                                        callback_data=str(call.message.id) + 'newmaster' + call.data)
                keyboard1.add(key_master)
                app1 = emoji.emojize(":blue_circle:") + '<b>Заявка № </b>' + str(
                    app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + "\nКомментарий: " + app.comment
                bot.send_message(call.from_user.id, app1, reply_markup=keyboard1, parse_mode="html")
                app2 = emoji.emojize(":blue_circle:") + '<b>Заявка № </b>' + str(
                    app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: договаривается ' + app.master + " " + app.master_surname
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=app2,
                                      parse_mode="html")
                try:
                    delete_from_sheet(int(app.nomer))
                    add_to_gsheet(call.message.chat.id, app.nomer, app.dataapp, app.city, app.equipment,
                                  app.damage, app.comment, app.number,
                                  app.name,
                                  str(app.master + " " + app.master_surname), "договаривается", None, None, None)
                except Exception:
                    return
        except Exception:
            bot.send_message(chat_id=call.from_user.id, text="Вам необходимо зарегистрироваться")


def process_password(message):
    try:
        global user_name, name, admin, chat_id13, administr
        if str(message.text) == "Rv6Qy49":
            msg = bot.reply_to(message, 'Введите имя')
            administr = "yes"
            bot.register_next_step_handler(msg, process_name_step)
        else:
            bot.reply_to(message, 'Пароль введен неверно')
    except Exception:
        return


def process_name_step(message):
    try:
        global user_name, name, admin, chat_id13
        name = message.text
        user_name = name
        admin = "yes"
        msg = bot.reply_to(message, 'Введите фамилию')
        bot.register_next_step_handler(msg, process_surname_step)
    except Exception as e:
        return


def process_name_master_step(message):
    try:
        global user_name, chat_id13, name
        name = message.text
        userclose = Userchat_forclose(name)
        users_dict[int(message.from_user.id)] = userclose
        user_name = name
        userclose.admin = "no"
        msg = bot.reply_to(message, 'Введите фамилию')
        bot.register_next_step_handler(msg, process_surname_master_step)
    except Exception as e:
        return


def process_surname_master_step(message):
    try:
        global chat_id13
        surname = message.text
        idd = message.chat.id
        idd1 = int(message.from_user.id)
        master = "yes"

        conn = sqlite3.connect('users.sql')
        conn_chat = sqlite3.connect('users_chat.sql')
        cur = conn.cursor()
        cur_chat = conn_chat.cursor()
        conn_close = sqlite3.connect('closes.sql')
        cur_close = conn_close.cursor()

        cur.execute("INSERT INTO users (name, surname, master) VALUES ('%s','%s','%s')" % (name, surname, master))
        cur_chat.execute("INSERT INTO users_chat (id, name, surname, master) VALUES ('%s','%s','%s','%s')" % (
            idd, name, surname, master))
        cur_close.execute("INSERT INTO closes (id, name, surname, master) VALUES ('%s','%s','%s','%s')" % (
            idd1, name, surname, master))
        conn_close.commit()
        conn_chat.commit()
        conn.commit()
        cur_close.close()
        cur.close()
        cur_chat.close()
        conn.close()
        conn_close.close()
        conn_chat.close()
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы мастером")
    except Exception as e:
        return


def process_surname_step(message):
    try:
        global chat_id13, administr, name
        surname = message.text
        chat_id13 = chat_id13 + 1
        idd = message.chat.id
        idd1 = int(message.from_user.id)
        if administr == "yes":
            print("aa")
            administr = str(message.chat.id)
            admin = "yes"
            master = "no"

            conn = sqlite3.connect('users.sql')
            conn_chat = sqlite3.connect('users_chat.sql')
            conn_close = sqlite3.connect('closes.sql')
            cur = conn.cursor()
            cur_chat = conn_chat.cursor()
            cur_close = conn_close.cursor()

            cur.execute(
                "INSERT INTO users (name, surname,master, admin, administr) VALUES ('%s','%s','%s','%s','%s')" % (
                    name, surname, master, admin, administr))
            cur_chat.execute(
                "INSERT INTO users_chat (id, name, surname,master, admin, administr) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    idd, name, surname, master, admin, administr))
            cur_close.execute(
                "INSERT INTO closes (id, name, surname,master, admin, administr) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    idd1, name, surname, master, admin, administr))
            conn_close.commit()
            conn_chat.commit()
            conn.commit()
            cur_close.close()
            cur.close()
            cur_chat.close()
            conn.close()
            conn_close.close()
            conn_chat.close()
            bot.send_message(message.chat.id, "Вы успешно зарегистрированы администрацией")
        else:
            db_users()
            for i in range(1, len(user_dict) + 1):
                user = user_dict[int(i)]
                if user.administr is not None:
                    flag = user.administr
                    adm = surname + " " + name + " регистрируется под админа"
                    keyboard1 = types.InlineKeyboardMarkup()
                    text = str(name) + " " + surname
                    key_yes = types.InlineKeyboardButton(text='Подтвердить',
                                                         callback_data=text + 'take' + str(message.chat.id))
                    key_no = types.InlineKeyboardButton(text='Отклонить',
                                                        callback_data=surname + 'dont' + str(message.chat.id))
                    keyboard1.add(key_yes)
                    keyboard1.add(key_no)
                    admin = "yes"
                    master = "delete"

                    conn = sqlite3.connect('users.sql')
                    conn_chat = sqlite3.connect('users_chat.sql')
                    conn_close = sqlite3.connect('closes.sql')
                    cur = conn.cursor()
                    cur_chat = conn_chat.cursor()
                    cur_close = conn_close.cursor()

                    cur.execute("INSERT INTO users (name, surname,master, admin) VALUES ('%s','%s','%s','%s')" % (
                        name, surname, master, admin))
                    cur_chat.execute(
                        "INSERT INTO users_chat (id, name, surname,master, admin) VALUES ('%s','%s','%s','%s','%s')" % (
                            idd, name, surname, master, admin))
                    cur_close.execute(
                        "INSERT INTO closes (id, name, surname,master, admin) VALUES ('%s','%s','%s','%s','%s')" % (
                            idd1, name, surname, master, admin))
                    conn_close.commit()
                    conn_chat.commit()
                    conn.commit()
                    cur_close.close()
                    cur.close()
                    cur_chat.close()
                    conn.close()
                    conn_close.close()
                    conn_chat.close()
                    bot.send_message(str(flag), adm, reply_markup=keyboard1)
                    bot.send_message(message.chat.id, "Ваша роль отправлена в администрацию на подтверждение")
    except Exception as e:
        return


# add row with request to sheet
def add_to_gsheet(message, text, text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1
    # noinspection PyBroadException
    try:
        # убрать если нужно чтобы была реакция при ЛС боту
        if message.chat.type == 'private':
            return
    except Exception:
        pass
    wks.append_row(
        [text, text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12])
    add_to_gsheet(message.chat.id, text, text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11,
                  text12)


# delete row from google sheets
def delete_from_sheet(j):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1

    try:
        for i in range(2, int(wks.row_count) + 1):
            if int(wks.cell(i, 1).value) == j:
                wks.delete_rows(i, i)
                break
    except Exception:
        return


@bot.message_handler(commands=['app'])
def add_bid(message):
    if message.chat.id == chat_chat:
        bot.delete_message(message.chat.id, message.id)
    keyboard1 = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard1.add(key_yes)
    question = 'Хотите оставить заявку?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard1)


def process_city_step(message):
    try:
        global chat_id12, city, name
        city = message.text
        conn = sqlite3.connect('users_chat.sql')
        cur = conn.cursor()
        cur.execute('SELECT id FROM users_chat WHERE id=?', (message.chat.id,))
        nooo = int(cur.fetchall()[0][0])
        conn.commit()
        cur.close()
        conn.close()
        user = user_chat_dict[nooo]
        name = str(str(user.name) + " " + str(user.surname))

        msg = bot.reply_to(message, 'Какая техника?')
        bot.register_next_step_handler(msg, process_equipment_step)
    except Exception as e:
        bot.reply_to(message, 'Зарегистрируйтесь, для того чтобы оставить заявку')


def process_equipment_step(message):
    try:
        global equipment
        equipment = message.text
        msg = bot.reply_to(message, 'Какая поломка?')
        bot.register_next_step_handler(msg, process_damage_step)
    except Exception as e:
        return


def process_damage_step(message):
    try:
        global damage
        damage = message.text
        msg = bot.reply_to(message, 'Введите контактный номер')
        bot.register_next_step_handler(msg, process_comment_step)
    except Exception as e:
        return


def process_comment_step(message):
    try:
        global number
        number = message.text
        msg = bot.reply_to(message, 'Напишите комментарий')
        bot.register_next_step_handler(msg, process_number_step)
    except Exception as e:
        return


def process_number_step(message):
    try:
        global chat1, chat_id12, number, status, comment
        chat1 = message.chat.id
        comment = message.text
        status = "нет"
        dat = str(date.today())
        msgadm = int(message.from_user.id)

        conn = sqlite3.connect('app.sql')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO app (dataapp, city, equipment, damage, comment, number, name, status,msgadm) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                dat, city, equipment, damage, comment, number, name, status, msgadm))
        conn.commit()
        cur.close()
        conn.close()

        conn = sqlite3.connect('app.sql')
        cur = conn.cursor()
        cur.execute('SELECT id FROM app ORDER BY id DESC LIMIT 1')
        nooo = int(cur.fetchall()[0][0])
        conn.commit()
        cur.close()
        conn.close()

        db_app()
        app = app_dict[nooo]
        keyboard1 = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Беру', callback_data=nooo)
        key_no = types.InlineKeyboardButton(text='Закрыть', callback_data='close' + str(nooo))
        keyboard1.add(key_yes)
        keyboard1.add(key_no)
        app1 = emoji.emojize(":red_circle:") + '<b>Новая заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment
        msg = bot.send_message(chat_chat, app1, reply_markup=keyboard1, parse_mode="html")
        conn = sqlite3.connect('app.sql')
        cur = conn.cursor()

        cur.execute("UPDATE app SET message = ? WHERE id = ?",
                    (int(str(msg.id)), nooo))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, text="Заявка отправлена")
        add_to_gsheet(message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage, app.comment,
                      app.number,
                      app.name, None,
                      None, None, None, None)
    except Exception as e:
        return


# post request second time if master didn't find
def process_newmaster(message):
    try:
        global chat_id12, second_id, msgID, msgID_second
        db_app()
        conn_app = sqlite3.connect('app.sql')
        cur = conn_app.cursor()
        cur.execute(
            "UPDATE app SET status = ? WHERE id = ?",
            ("нет", msgID)
        )
        conn_app.commit()
        cur.close()
        conn_app.close()
        db_app()
        app = app_dict[msgID]
        app.status = "нет"
        keyboard1 = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Беру', callback_data=msgID)
        key_no = types.InlineKeyboardButton(text='Закрыть', callback_data='close')
        keyboard1.add(key_yes)
        keyboard1.add(key_no)
        app1 = emoji.emojize(":red_circle:") + ' <b>Новая заявка № </b> ' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: актуальная ' + '\nПримечание: ' + message.text + " (" + app.master + " " + app.master_surname + ")"
        app2 = emoji.emojize(":blue_circle:") + ' <b>Заявка № </b> ' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + "\nКомментарий: " + app.comment + '\nСтатус: переоформлена на новую ' + '\nПримечание: ' + message.text
        bot.edit_message_text(chat_id=chat_chat, message_id=second_id, text=app1, reply_markup=keyboard1,
                              parse_mode="html")
        bot.edit_message_text(chat_id=message.chat.id, message_id=msgID_second, text=app2, parse_mode="html")
        bot.send_message(message.chat.id, "Статус заявки обновился на новую")
    except Exception as e:
        return


# set status to 'не договорился'
def process_no_accept(message):
    try:
        global chat_id12, second_id, msgID
        db_app()
        conn_app = sqlite3.connect('app.sql')
        cur = conn_app.cursor()
        cur.execute(
            "UPDATE app SET status = ? WHERE id = ?",
            ("закрыта, не договорился", msgID)
        )
        conn_app.commit()
        cur.close()
        conn_app.close()
        db_app()
        app = app_dict[msgID]
        app.status = "закрыта, не договорился"
        app1 = emoji.emojize(":black_circle:") + '<b>Заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: закрыта. ' + '\nПримечание: ' + message.text + ' (' + app.master + " " + app.master_surname + ")"
        app2 = emoji.emojize(":black_circle:") + '<b>Заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + "\nКомментарий: " + app.comment + '\nСтатус: закрыта,не договорился ' + '\nПримечание: ' + message.text + ' (' + app.master + " " + app.master_surname + ")"
        bot.edit_message_text(chat_id=chat_chat, message_id=second_id, text=app1, parse_mode="html")
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 2, text=app2, parse_mode="html")
        bot.send_message(message.chat.id, "Заявка закрыта")
        text = "закрыта, не договорился. " + str(message.text)
        delete_from_sheet(int(app.nomer))
        add_to_gsheet(message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage, app.comment,
                      app.number,
                      app.name,
                      str(app.master + " " + app.master_surname), text, None, None, None)
    except Exception as e:
        return


text_table = None


# ask percent from master
def process_complete(message):
    try:
        global text_table
        db_app()
        app = app_dict[second_id]
        text = "Введите сумму процента (30% от чистой прибыли) для заявки № " + str(app.nomer)
        text_table = str(message.text)
        app1 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, ремонт выполнен' + ' (' + app.master + " " + app.master_surname + ")" + "\nПримечание: " + message.text
        bot.edit_message_text(app1, chat_id=chat_chat, message_id=int(app.message), parse_mode="html")
        msg = bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(msg, process_send)
    except Exception:
        return


# send percent to admin
def process_send(message):
    try:
        global second_id, percent, msgID, text_table
        db_app()
        percent = str(message.text)
        text2 = str(percent)
        text4 = "После того, как отправите процент администратору, нажмите кнопку процент отправлен, " \
                "после подтверждения перевода администратором, заявка будет закрыта. "
        conn_app = sqlite3.connect('app.sql')
        cur = conn_app.cursor()
        cur.execute(
            "UPDATE app SET status = ? WHERE id = ?",
            ("закрыта ремонтом", second_id)
        )
        conn_app.commit()
        cur.close()
        conn_app.close()
        db_app()
        app = app_dict[second_id]
        text1 = "закрыта ремонтом." + str(text_table)
        app2 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, ремонт выполнен' + ' (' + app.master + " " + app.master_surname + ") "
        keyboard1 = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='% отправлен',
                                             callback_data='send' + str(second_id))
        keyboard1.add(key_yes)
        bot.edit_message_text(chat_id=message.chat.id, message_id=msgID, text=app2,
                              reply_markup=keyboard1, parse_mode="html")
        bot.send_message(message.chat.id, text4)
        delete_from_sheet(int(app.nomer))
        add_to_gsheet(message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage, app.comment,
                      app.number, app.name,
                      str(app.master + " " + app.master_surname), text1, text2, None, None)
    except Exception as e:
        return


# set status to 'диагностика'
def process_diagn(message):
    try:
        global second_id, msgID, msgID_second
        app = app_dict[second_id]
        app1 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, диагностика' + ' (' + app.master + " " + app.master_surname + ")" + "\nПримечание: " + message.text
        app2 = emoji.emojize(":green_circle:") + '<b>Заявка № </b>' + str(
            app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + "\nКомментарий: " + app.comment + '\nСтатус: закрыта, диагностика' + ' (' + app.master + " " + app.master_surname + ")" + "\nПримечание: " + message.text
        bot.edit_message_text(chat_id=chat_chat, message_id=msgID, text=app1,
                              parse_mode="html")
        bot.edit_message_text(chat_id=message.chat.id, message_id=msgID_second, text=app2,
                              parse_mode="html", reply_markup=None)
        status = 'закрыта, диагностика.' + str(message.text)
        delete_from_sheet(int(app.nomer))
        add_to_gsheet(message.chat.id, app.nomer, app.dataapp, app.city, app.equipment, app.damage,
                      app.comment,
                      app.number,
                      app.name,
                      str(app.master + " " + app.master_surname),
                      status, None, None, None)
    except Exception as a:
        return


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()


# command new which show new requests
@bot.message_handler(commands=['new'])
def new1(msg):
    db_app()
    count = 0
    bot.delete_message(msg.chat.id, msg.id)
    for i in range(1, len(app_dict) + 1):
        app = app_dict[i]
        if app.status == "нет":
            count += 1
            keyboard1 = types.InlineKeyboardMarkup()
            key_yes = types.InlineKeyboardButton(text='Беру', callback_data=i)
            key_no = types.InlineKeyboardButton(text='Закрыть', callback_data='close' + str(i))
            keyboard1.add(key_yes)
            keyboard1.add(key_no)
            app1 = emoji.emojize(":red_circle:") + '<b>Новая заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment
            msg = bot.send_message(chat_chat, app1, reply_markup=keyboard1, parse_mode="html")
            bot.delete_message(chat_chat, int(str(app.message)))
            conn = sqlite3.connect('app.sql')
            cur = conn.cursor()

            cur.execute("UPDATE app SET message = ? WHERE id = ?",
                        (int(str(msg.id)), i))
            conn.commit()
            cur.close()
            conn.close()
    if count == 0:
        bot.send_message(msg.chat.id, "Новых заявок на данный момент нет")


# command mastera which show requests of each masters
@bot.message_handler(commands=['mastera'])
def saw(message):
    db_users()
    db_app()
    if message.chat.id == chat_chat:
        bot.delete_message(message.chat.id, message.id)
    for i in range(1, len(user_dict) + 1):
        dogov = 0
        nedogov = 0
        close = 0
        diagn = 0
        count = 0
        client = 0
        apps = []
        user = user_dict[int(i)]
        if user.master == "yes":
            for j in range(1, len(app_dict) + 1):
                app = app_dict[int(j)]
                if app.master_surname == user.surname:
                    if app.status == "договаривается" or app.status == "договорился":
                        dogov = dogov + 1
                    elif app.status == "закрыта, не договорился":
                        nedogov = nedogov + 1
                    elif app.status == "закрыта ремонтом":
                        close = close + 1
                        apps.append(app.nomer)
                    elif app.status == "закрыта, отчитана":
                        count = count + 1
                    elif app.status == "закрыта, диагностика":
                        diagn += 1
                    elif app.status == "клиент отменил заявку":
                        client += 1
            bot.send_message(message.from_user.id,
                             text="Мастер " + str(user.name) + " " + str(user.surname) + ": \nв работе: " + str(
                                 dogov) + "\nне договорился: " + str(
                                 nedogov) + "\nдиагностика: " + str(diagn) + "\nзакрыто ремонтом, не отчитана: " + str(
                                 close) + str(apps) + "\nзакрыто ремонтом, отчитана: " + str(
                                 count) + "\nклиент отменил заявку: " + str(client))


# command see, which show how many request master has
@bot.message_handler(commands=['see'])
def see1(msg):
    db_app()
    db_users_chat()
    user = user_chat_dict[int(msg.from_user.id)]
    count = 0
    count_adm = 0
    if msg.chat.id == chat_chat:
        bot.delete_message(msg.chat.id, msg.id)
    for i in range(1, len(app_dict) + 1):
        app = app_dict[i]
        if (
                app.status == "договорился" or app.status == "закрыта, ремонт выполнен") and app.master == user.name and app.master_surname == user.surname:
            app1 = emoji.emojize(":blue_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + "\nКомментарий: " + app.comment + '\nПоломка: ' + app.damage + '\nТелефон: ' + app.number + '\nСтатус: в работе'
            count += 1
            bot.send_message(msg.from_user.id, app1, parse_mode="html")
        if user.admin == "yes" and app.status == "договорился" or app.status == "закрыта, ремонт выполнен":
            count_adm += 1
            app1 = emoji.emojize(":blue_circle:") + '<b>Заявка № </b>' + str(
                app.nomer) + '\nГород: ' + app.city + '\nТехника: ' + app.equipment + '\nПоломка: ' + app.damage + "\nКомментарий: " + app.comment + '\nСтатус: в работе' + "\nМастер: " + app.master + " " + app.master_surname
            bot.send_message(msg.from_user.id, app1, parse_mode="html")
    if count == 0 and user.master == "yes":
        bot.send_message(msg.from_user.id, "Заявок в работе на данный момент нет")
    if count_adm == 0 and user.admin == "yes":
        bot.send_message(msg.from_user.id, "Заявок в работе на данный момент нет")


bot.polling(none_stop=True)
