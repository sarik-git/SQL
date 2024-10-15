import telebot
import buttons15_2 as bt
import database15_2 as db

bot = telebot.TeleBot('7870136037:AAE8W0Dl2DkLQUEEBIAvgNlkprFH0WqhqDM')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.check_user(user_id):
        bot.send_message(user_id, 'Привет!')
    else:
        bot.send_message(user_id, 'Привет! Давайте начнем регистрацию!\n'
                                  'Введите ваше Имя!')
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(commands=['greet'])
def greetings(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f'Добро пожаловать {message.from_user.username}')


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, f'Отлично {user_name}! Теперь отправьте свой номер через кнопку!', reply_markup=bt.number_button())
    bot.register_next_step_handler(message, get_number, user_name)


def get_number(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        bot.send_message(user_id, 'Вы успешно зарегистрированы! Теперь отправьте свою локацию через кнопку!', reply_markup=bt.location_button())
        bot.register_next_step_handler(message, get_location, user_name)
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку ниже!')
        bot.register_next_step_handler(message, get_number, user_name)


def get_location(message, user_name):
    user_id = message.from_user.id
    if message.location:
        bot.send_message(user_id, 'Вы успешно зарегистрированы!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку ниже!')
        bot.register_next_step_handler(message, get_location, user_name)


bot.polling()