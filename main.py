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


def send(mail):
    bot = telebot.TeleBot(TOKEN)
    if mail['mail_type'] == 'test':
        ids = ADMIN_IDS
    else:
        ids = get_ids()

    message = get_message(mail['text_file'])

    if mail['photo_file'] is None:
        for id in ids:
            try:
                bot.send_message(id, message, disable_web_page_preview=mail['disable_preview'])
            except Exception as e:
                pass
    else:
        with open(f"messages/{mail['photo_file']}", 'rb') as photo:
            for id in ids:
                try:
                    bot.send_photo(id, photo, caption=message)
                except Exception as e:
                    pass

    print('Done')
    return schedule.CancelJob


def schedule_sending(mail):
    schedule.every().day.at(mail['time']).do(send, mail)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    if mail['mail_type'] == 'test':
        send(mail)
    if mail['mail_type'] == 'main':
        schedule_sending(mail)
