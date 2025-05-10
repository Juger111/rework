import telebot  # библиотека telebot
from config import token  # импорт токена

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


# 🔥 Новый хэндлер: бан за ссылку
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'video_note'])
def check_for_links(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = bot.get_chat_member(chat_id, user_id).status

    # Получаем текст из сообщения или подписи к медиа
    text = message.text or message.caption

    # Если есть текст и в нем есть ссылка
    if text and ("http://" in text or "https://" in text or "t.me/" in text):
        if user_status not in ['administrator', 'creator']:
            try:
                username = message.from_user.username or message.from_user.first_name
                bot.ban_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь @{username} был забанен за отправку ссылки.")
                print(f"Забанен: {username}")
            except Exception as e:
                print(f"Ошибка при бане: {e}")
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        bot.send_message(message.chat.id, f"Добро пожаловать, {new_member.first_name}!")
        try:
            bot.approve_chat_join_request(message.chat.id, new_member.id)  # для супергрупп с ручным одобрением
        except Exception as e:
            print(f"Запрос на вступление не был одобрен (возможно, не требуется): {e}")

bot.infinity_polling(none_stop=True)
