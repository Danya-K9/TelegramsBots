import telebot
from telebot import types
import config
import re
import os
import random

bot = telebot.TeleBot(config.TOKEN)
waiting_for_comment = {}
waiting_for_order = {}
admin_id1 = 1962376006
admin_id = 5722086301

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton("Прайс-лист")
    item2 = types.KeyboardButton("Заказать товар")
    markup.row(item1, item2)
    markup.add(types.KeyboardButton("Отмена"))
    markup.add(types.KeyboardButton("Розыгрыши"))
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f"Привет, {user_name}! Я бот-ассистент Вейп Шопа. Выберите одну из кнопок для дальнейшего действия:", reply_markup=markup)
    print(f'Получено сообщение от пользователя {message.from_user.first_name} {user_id}: {message.text}')

@bot.message_handler(commands=['Admin'])
def admin_command(message):
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    if message.from_user.id == admin_id:
        global files
        files = [file for file in os.listdir() if file.endswith(".txt")]  # Получаем список всех текстовых файлов в текущей директории
        files_list = "\n".join(files) if files else "Нет текстовых файлов в текущей директории."
        bot.send_message(admin_id, f"Список текстовых файлов:\n{files_list}")
        print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    elif message.from_user.id == admin_id1:
        #global files
        files = [file for file in os.listdir() if
                 file.endswith(".txt")]  # Получаем список всех текстовых файлов в текущей директории
        files_list = "\n".join(files) if files else "Нет текстовых файлов в текущей директории."
        bot.send_message(admin_id1, f"Список текстовых файлов:\n{files_list}")
        print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    else:
        bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды.")


@bot.message_handler(commands=['Read'])
def read_file(message):
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    if message.from_user.id == admin_id or message.from_user.id == admin_id1:
        bot.send_message(message.chat.id, "Пожалуйста, укажите название файла, который вы хотите прочитать.")
        bot.register_next_step_handler(message, process_file)
    else:
        bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды.")
def process_file(message):
    try:
        file_name = message.text.strip()
        with open(file_name, 'r') as file:
            file_content = file.read()
            bot.send_message(message.chat.id, f"Содержимое файла '{file_name}':\n{file_content}")
    except FileNotFoundError:
        bot.send_message(message.chat.id, f"Файл '{file_name}' не найден. Пожалуйста, укажите корректное название файла.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при чтении файла: {str(e)}")

@bot.message_handler(commands=['File'])
def change_file_command(message):
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, "Введите название файла, который вы хотите изменить:")
        bot.register_next_step_handler(message, handle_file_input)
        print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    elif message.from_user.id == admin_id1:
        bot.send_message(admin_id1, "Введите название файла, который вы хотите изменить:")
        bot.register_next_step_handler(message, handle_file_input)
        print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    else:
        bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды.")

def handle_file_input(message):
    selected_file = message.text
    bot.send_message(admin_id, f"Введите текст, который вы хотите сохранить в файле '{selected_file}':")
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    bot.register_next_step_handler(message, lambda msg: handle_text_input(msg, selected_file))

def handle_text_input(message, selected_file):
    text_to_write = message.text
    file_path = os.path.join(os.path.dirname(__file__), selected_file)
    with open(file_path, 'rb') as file:  # Используем бинарный режим чтения
        file_content = file.read().decode('utf-8')  # Декодируем содержимое файла с указанием кодировки
    with open(file_path, 'wb') as file:
        file.write(text_to_write.encode('utf-8'))
    bot.send_message(admin_id, f"Текст успешно сохранен в файле '{selected_file}'.")



@bot.message_handler(func=lambda message: message.text.lower() == "розыгрыши")
def cancel_action(message):
    user_id = message.from_user.id
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    bot.send_message(user_id, "По случаю запуска нашего телеграм-бота Ease_Vape мы решили разыграть между вами 2 банки жидкости. Всего 2 победителя! Условия конкурса очень просты:\n\n1. Нужно быть подписанным на телеграм-канал Ease Vape (ссылка на группу: https://t.me/Easevape).\n2. Заказать и купить любой товар через бота.\n3. Обязательно указать свой телеграм-аккаунт при оформлении заказа.\n\nПри этом вы получите номер, который будет участвовать в розыгрыше. Чем больше вы купите товаров, тем больше номеров вы получите, и тем выше будет ваш шанс на победу!\nP.S. Всегда заказывайте товар через один и тот же телеграмм-аккаунт.\n\n1 товар - 1 номер.\n\nИтоги подведем ровно через две недели. Желаем Удачи!")
    bot.send_message(user_id, "Первое место: ‼️Padonki Vintage пинаколада с грушей 20 mg strong‼️\nВторое место: ‼️Hot Spot Fuel Up Гуава морошко 50 mg strong‼️")

@bot.message_handler(func=lambda message: message.text.lower() == "отмена")
def cancel_action(message):
    user_id = message.from_user.id
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    if waiting_for_order.get(user_id):
        waiting_for_order.pop(user_id)
        bot.send_message(user_id, "Действие отменено. Вы вернулись к основному меню.")
    else:
        bot.send_message(user_id, "Нет активных действий для отмены.")
@bot.message_handler(func=lambda message: message.text == "Заказать товар")
def request_order_info(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    item_da = types.InlineKeyboardButton('Да', callback_data='confirm_order')
    item_net = types.InlineKeyboardButton('Нет', callback_data='cancel_order')
    markup.row(item_da, item_net)

    bot.send_message(user_id, "Вы ознакомились с наличием товара и его ценами?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_order')
def confirm_order(call):
    user_id = call.from_user.id
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.send_message(user_id, "Укажите количество товара, который вы хотите заказать? (Например: 3)")
    print(f'Получено сообщение от пользователя {user_id}: {call.from_user.first_name}: {call.data}')
    waiting_for_order[user_id] = {"user_id": user_id, "user_name": call.from_user.first_name, "num": None, "product": None, "date": None, "time": None, "change": None, "location": None, "phone": None}

@bot.message_handler(func=lambda message: waiting_for_order.get(message.from_user.id) and waiting_for_order[message.from_user.id]["num"] is None)
def handle_product(message):
    user_id = message.from_user.id
    num_input = message.text
    if not num_input.isdigit():
        bot.send_message(user_id, "Пожалуйста, введите только цифры для количества товара.")
        return
    waiting_for_order[user_id]["num"] = num_input
    bot.send_message(user_id, "Что бы вы хотели заказать? Например: Жидкость HotSpot ACID кислое яблоко, Картридж на xros 0.6. (Обратите внимание: если вы не будете вводить корректно данные по форме, ваш заказ будет автоматически отменен.)")
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_order')
def cancel_order(call):
    user_id = call.from_user.id
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.send_message(user_id, "Действие отменено. Пожалуйста, изучите прайс-лист перед оформлением заказа. Для просмотра прайс-листа нажмите на кнопку 'Прайс-лист'")

@bot.message_handler(func=lambda message: waiting_for_order.get(message.from_user.id) and waiting_for_order[message.from_user.id]["product"] is None)
def handle_product(message):
    user_id = message.from_user.id
    waiting_for_order[user_id]["product"] = message.text
    bot.send_message(user_id, "Укажите дату для встречи (например, 26.10.2024):")
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')

@bot.message_handler(func=lambda message: waiting_for_order.get(message.from_user.id) and waiting_for_order[message.from_user.id]["date"] is None)
def handle_date(message):
    user_id = message.from_user.id
    date_pattern = r"\d{2}\.\d{2}\.\d{4}"
    if re.match(date_pattern, message.text):
        waiting_for_order[user_id]["date"] = message.text
        bot.send_message(user_id, "Укажите время встречи (например, 17:00):")
    else:
        bot.send_message(user_id, "Неверный формат даты. Пожалуйста, введите дату в формате дд.мм.гггг.")

@bot.message_handler(func=lambda message: waiting_for_order.get(message.from_user.id) and waiting_for_order[message.from_user.id]["time"] is None)
def handle_time(message):
    user_id = message.from_user.id
    time_pattern = r"\d{2}:\d{2}"
    if re.match(time_pattern, message.text):
        waiting_for_order[user_id]["time"] = message.text
        bot.send_message(user_id, "Укажите сумму для сдачи (если сдача не нужна, напишите '0'):")
    else:
        bot.send_message(user_id, "Неверный формат времени. Пожалуйста, введите время в формате чч:мм.")


@bot.message_handler(func=lambda message: waiting_for_order.get(message.from_user.id) and waiting_for_order[message.from_user.id]["change"] is None)
def handle_change(message):
    user_id = message.from_user.id
    change = message.text
    if re.match(r"^\d+([\.,]?\d{0,2})?$", change):  # Проверяем, что сумма для сдачи содержит только цифры, возможно точку или запятую
        change = change.replace(',', '.')  # Заменяем запятую на точку для унификации формата
        waiting_for_order[user_id]["change"] = change
        bot.send_message(user_id, "Укажите, пожалуйста, нам свой Telegram (пример: @Ease_VapeBot) или номер телефона для дальнейшего взаимодействия. (P.S. Лучше оставьте Telegram и номер телефона сразу, так будет проще нам с вами связаться для решения любых проблем).")
        print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')
    else:
        bot.send_message(user_id, "Сумма для сдачи должна содержать только цифры, запятую или точкку. Пожалуйста, введите сумму сдачи заново.")

@bot.message_handler(func=lambda message: waiting_for_order.get(message.from_user.id) and waiting_for_order[message.from_user.id]["phone"] is None)
def handle_phone(message):
    user_id = message.from_user.id
    waiting_for_order[user_id]["phone"] = message.text

    markup = types.InlineKeyboardMarkup()
    item_dkl = types.InlineKeyboardButton('ДКЛ', callback_data='dkl')
    item_5_element = types.InlineKeyboardButton('5 Элемент', callback_data='5_element')
    item_dom_torgovli = types.InlineKeyboardButton('Дом торговли', callback_data='dom_torgovli')
    markup.row(item_dkl, item_5_element)
    markup.row(item_dom_torgovli)

    bot.send_message(user_id, "Выберите место доставки:", reply_markup=markup)
    print(f'Получено сообщение от пользователя {message.from_user.first_name}: {message.text}')

@bot.callback_query_handler(func=lambda call: call.data in ['dkl', '5_element', 'dom_torgovli'])
def handle_delivery_location(call):
    user_id = call.from_user.id
    location = ""

    if call.data == 'dkl':
        location = "ДКЛ"
    elif call.data == '5_element':
        location = "5 Элемент"
    elif call.data == 'dom_torgovli':
        location = "Дом торговли"

    waiting_for_order[user_id]["location"] = location
    bot.send_message(user_id, f"Место доставки успешно выбрано: {location}")

    bot.edit_message_reply_markup(user_id, call.message.message_id)

    # Запрос подтверждения заказа
    markup = types.InlineKeyboardMarkup()
    item_dad = types.InlineKeyboardButton('Да', callback_data='da')
    item_nett = types.InlineKeyboardButton('Нет', callback_data='net')
    markup.row(item_dad, item_nett)

    bot.send_message(user_id, "Подтвердите ваш заказ:\n"
                              f"Количество товара: {waiting_for_order[user_id]['num']}\n"
                              f"Товар: {waiting_for_order[user_id]['product']}\n"
                              f"Дата: {waiting_for_order[user_id]['date']}\n"
                              f"Время: {waiting_for_order[user_id]['time']}\n"
                              f"Сдача: {waiting_for_order[user_id]['change']}\n"
                              f"Номер: {waiting_for_order[user_id]['phone']}\n"
                              f"Место: {waiting_for_order[user_id]['location']}\n"
                              "Отправьте 'Да', чтобы подтвердить, или 'Нет', чтобы отменить.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'da')
def confirm_order(call):
    user_id = call.from_user.id
    markup = types.InlineKeyboardMarkup()
    item_confirm = types.InlineKeyboardButton('Одобрить', callback_data='confirm')
    item_cancel = types.InlineKeyboardButton('Отменить заказ', callback_data='cancel')
    markup.row(item_confirm, item_cancel)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    order_info = waiting_for_order[user_id]
    bot.send_message(user_id, "Заказ успешно оформлен! Вы получите уведомление о подтверждении заказа, либо мы свяжемся с вами для его подтверждения.")
    order_summary = f"ID: {order_info['user_id']}\nИмя: {order_info['user_name']}\nКол-во товара: {order_info['num']}\nТовар: {order_info['product']}\nДата: {order_info['date']}\nВремя: {order_info['time']}\nСдача: {order_info['change']}\nМесто: {order_info['location']}\nСвязь: {order_info['phone']}"

    #bot.send_message(5722086301, order_summary, reply_markup=markup)
    bot.send_message(1962376006, order_summary, reply_markup=markup)
   #bot.send_message(759233229, order_summary, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm')
def confirm(call):
    admin_idJ = 5722086301
    admin_idK = 1962376006
    admin_id = call.from_user.id
    user_id = int(call.message.text.split('\n')[0].split(': ')[1])  # Получаем ID пользователя из текста сообщения
    user_name = call.message.text.split('\n')[1].split(': ')[1]  # Получаем имя пользователя из текста сообщения
    phone_number = call.message.text.split('\n')[-1].split(': ')[1]  # Получаем номер телефона пользователя из текста сообщения
    num_of_items = int(call.message.text.split('\n')[2].split(': ')[1])  # Получаем количество товара
    bot.send_message(user_id, f"Привет, {user_name}! Ваш заказ одобрен! Ждем тебя в назначенное время и месте.")
    bot.edit_message_reply_markup(chat_id=admin_idK, message_id=call.message.message_id, reply_markup=None)
    bot.send_message(admin_idK, f"Заказ пользователя {user_name} (ID: {user_id}) одобрен.")
    save_data(user_name, user_id, phone_number, num_of_items)

def save_data(user_name, user_id, phone_number, num_of_items):
        with open('lottery.txt', 'a+') as file:
            file.seek(1)
            for _ in range(num_of_items):
                random_number = random.randint(1, 500)
                file.write(f'{user_id}:{user_name}:{phone_number}:{random_number}\n')
                print(f"Данные сохранены для пользователя {user_name} (ID: {user_id}, номер: {random_number}).")

admin_idK = 1962376006
@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def cancel_order(call):
    admin_idK = 1962376006
    bot.edit_message_reply_markup(chat_id=admin_idK, message_id=call.message.message_id, reply_markup=None)
    user_id = int(call.message.text.split('\n')[0].split(': ')[1])
    user_name = call.message.text.split('\n')[1].split(': ')[1]
    bot.send_message(user_id, f"{user_name} К сожалению, ваш заказ был отменен. Пожалуйста, перепроверьте информацию о заказе или наличие товара.")
    bot.send_message(admin_idK, f"Заказ: {user_name}, ID:{user_id} отменён.")





@bot.callback_query_handler(func=lambda call: call.data == 'net')
def net(call):
    user_id = call.from_user.id
    bot.send_message(user_id, "Заказ отменен. Вы можете начать заново, выбрав 'Заказать товар'.")
    waiting_for_order.pop(user_id)



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    print(f'Получено сообщение от пользователя {user_id}: {message.from_user.first_name}: {message.text}')
    if message.text == "Прайс-лист":
        bot.send_message(message.chat.id, "Какие товары ты хочешь посмотреть?😊\nУ нас есть такие товары:\n\n⛱️Жидкости⛱️: \n/GENETIC_CODE\n/HotSpot_FuelUp\n/HotSpot_ACID\n/CATSWILL\n/DUAL\n/RICK_AND_MORTY_BAD_TRIP\n/IndiviDUAL\n/Malaysia\n/Podonki_ALFAVAPE\n/Podonki_VINTAGE\n\n💨Картриджи и испарители💨:\n/Ispar\n/Cartridges\n\n⚫️Снюс⚫️:\n/Snus\n\n🚬Под-системы🚬\n/Xros_Mini")
    elif message.text == "Заказать товар":
        request_order_info(message)  # Вызываем функцию для запроса информации о заказе
    else:
        if message.text.startswith('/') and all(char.isalpha() or char in ['/', '_'] for char in message.text.lstrip('/')):
            file_name = message.text.lstrip('/') + ".txt"
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    bot.send_message(message.chat.id, file_content)
            except FileNotFoundError:
                bot.send_message(message.chat.id, "Такого товара не найдено. Выберите другой товар.")
        else:
            bot.send_message(message.chat.id, "Такого товара не найдено. Выберите другой товар.")
bot.polling(none_stop=True)


