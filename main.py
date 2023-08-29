import telebot
from config import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time


def get_ids():
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    cred_file = 'sheets_key.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
    client = gspread.authorize(credentials)
    sheet = client.open('user data').sheet1
    data = sheet.get_all_values()
    ids = []
    for i in data[1:]:
        if i[0] != '0':
            ids.append(int(i[0]))
    return ids


def get_message(name):
    with open(f'messages/{name}', "r", encoding="utf-8") as f:
        lines = f.readlines()
        return ''.join(lines)


def send(message, type='test'):
    bot = telebot.TeleBot(TOKEN)
    if type == 'test' or type == 'test_mail':
        ids = ADMIN_IDS
    else:
        ids = get_ids()
    text = get_message(message['TEXT_FILE'])

    if message['PHOTO_FILE'] is None:
        for id in ids:
            try:
                bot.send_message(id, text, disable_web_page_preview=message['DISABLE_PREVIEW'])
            except Exception as e:
                pass
    else:
        with open(f"messages/{message['PHOTO_FILE']}", 'rb') as photo:
            for id in ids:
                try:
                    bot.send_photo(id, photo, caption=text)
                except Exception as e:
                    pass
    print('sent')
    return schedule.CancelJob


def schedule_sending(mail):
    for m in mail['messages']:
        schedule.every().day.at(m['TIME']).do(lambda: send(m, mail['MAIL_TYPE']))
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    if mail['MAIL_TYPE'] == 'test' or mail['MAIL_TYPE'] == 'inst_mail':
        for m in mail['messages']:
            send(m, mail['MAIL_TYPE'])
    elif mail['MAIL_TYPE'] == 'mail' or mail['MAIL_TYPE'] == 'test_mail':
        schedule_sending(mail)
