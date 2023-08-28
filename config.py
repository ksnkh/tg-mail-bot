# все параметры записывать в '...' ковычках(тип переменной str), кроме None, True, False.
mail = {
    # имя файла в папке messages
    'text_file': 'message.txt',

    # имя фото в папке messages(если без фото, то None)
    'photo_file': None,

    # время рассылки в формате hh:mm
    'time': '14:00',

    # 'main' если надо разослать всем,
    # 'test' если надо проверить(сразу же отправится только определенным пользователям)
    'mail_type': 'main',

    # если в сообщении ссылка
    # True - спрятать (для zoom ссылок)
    # False - показывать (превьюхи Youtube)
    'disable_preview': False
}


# id админов/тестеров можно взять в гугл таблице
ADMIN_IDS = []


# main token
TOKEN = "TOKEN"
