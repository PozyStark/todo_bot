import telebot
import sqlite3

bot = telebot.TeleBot('Сюда необходимо посместить токен доступа')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/create':
        bot.send_message(message.from_user.id, 'Опишите задачу')
        bot.register_next_step_handler(message, get_task_description)
    elif message.text == '/tasks':
        get_all_tasks(message)
    elif message.text == '/delete':
        bot.send_message(message.from_user.id, 'Введите Id задачи')
        bot.register_next_step_handler(message, delete_task)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Список команд:\n '
                                               '/create-создать задачу\n'
                                               '/tasks-список всех задач\n'
                                               '/delete-удалить задачу по Id'
                         )
    else:
        bot.send_message(message.from_user.id, 'I dont understand you!')


def get_task_description(message):
    try:
        connection = sqlite3.connect('base')
        cursor = connection.cursor()
        task_description = message.text
        query = f"insert into user_task (user_id, task) values ({message.from_user.id}, '{task_description}')"
        cursor.execute(query)
        connection.commit()
        bot.send_message(message.from_user.id, f'Задача:{task_description} создана')
        cursor.close()
        connection.close()
    except sqlite3.Error as error:
        print(f'Error, cant connect to data base {error}')


def get_all_tasks(message):
    try:
        connection = sqlite3.connect('base')
        cursor = connection.cursor()
        query = f"select * from user_task where user_id={message.from_user.id}"
        cursor.execute(query)
        tasks = cursor.fetchall()
        response = 'Список задач\n'
        for index, task in enumerate(tasks):
            response += f'Задача Id:{task[0]} №{index}: {task[2]}\n'
        bot.send_message(message.from_user.id, response)
        cursor.close()
        connection.close()
    except sqlite3.Error as error:
        print(f'Error, cant connect to data base {error}')


def delete_task(message):
    try:
        task_id = message.text
        connection = sqlite3.connect('base')
        cursor = connection.cursor()
        query = f"delete from user_task where id={task_id}"
        cursor.execute(query)
        connection.commit()
        bot.send_message(message.from_user.id, f'Задача Id:{task_id} удалена.')
        cursor.close()
        connection.close()
    except sqlite3.Error as error:
        print(f'Error, cant connect to data base {error}')


bot.polling(none_stop=True, interval=0)
