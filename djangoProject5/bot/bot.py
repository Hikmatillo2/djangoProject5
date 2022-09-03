import telebot
from django.core.management.base import BaseCommand
from bot.models import *
from bot.keyboards import InlineKeyboard
from bot.translete_callbacks import translit

TOKEN = '5547312177:AAHXe2ZDglnTD7X-F6x7IlwQ-kO5mQYEHVs'
bot = telebot.TeleBot(TOKEN)

USER_CALLBACKS = ['growth_school', 'football', 'piktomir', 'robotics', 'cuboro', 'courses_nine_grade', 'wardrobe',
                  'questions', 'advanced_informatics', 'steps_for_success', 'english_first_grade', 'user_menu', 'menu',
                  'info_growth_school', 'groups_growth_school', 'booklet_growth_school', 'cost_growth_school',
                  'info_piktomir', 'groups_piktomir', 'booklet_piktomir', 'cost_piktomir',
                  'info_robotics', 'groups_robotics', 'cost_robotics',
                  'info_cuboro', 'groups_cuboro', 'booklet_cuboro', 'cost_cuboro',
                  'info_football', 'groups_football', 'booklet_football', 'cost_football',
                  'info_courses_nine_grade', 'groups_courses_nine_grade', 'booklet_courses_nine_grade',
                  'cost_courses_nine_grade',
                  'info_advanced_informatics', 'groups_advanced_informatics', 'booklet_advanced_informatics',
                  'cost_advanced_informatics',
                  'info_steps_for_success', 'groups_steps_for_success', 'booklet_steps_for_success',
                  'cost_steps_for_success',
                  'info_english_first_grade', 'groups_english_first_grade', 'booklet_english_first_grade',
                  'cost_english_first_grade', 'back', 'message', 'no_files',

                  'back_piktomir', 'back_growth_school', 'back_cuboro', 'back_wardrobe', 'back_steps_for_success',
                  'back_advanced_informatics', 'back_english_first_grade', 'yes_files', 'back_courses_nine_grade',
                  'back_robotics', 'back_football', 'hide']


class FilesLimitExceeded(Exception):
    pass


def message_for_admin(message):
    if message.text:
        if message.text == '/menu':
            menu_command(message)
        else:
            if not BotUser.objects.filter(user_id=message.chat.id) and not Condition.objects.filter(
                    user_id=message.chat.id):
                BotUser(user_id=message.chat.id,
                        first_name=message.from_user.first_name, last_name=message.from_user.last_name).save()
                Condition(user=BotUser.objects.get(user_id=message.chat.id)).save()

            elif not Condition.objects.filter(user_id=message.chat.id) and BotUser.objects.filter(
                    user_id=message.chat.id):
                Condition(user=BotUser.objects.get(user_id=message.chat.id)).save()

            elif Condition.objects.filter(user_id=message.chat.id) and not BotUser.objects.filter(
                    user_id=message.chat.id):
                BotUser(user_id=message.chat.id,
                        first_name=message.from_user.first_name, last_name=message.from_user.last_name).save()

            MessageBot(user=BotUser.objects.get(user_id=message.chat.id),
                       text=message.text).save()
            bot.send_message(message.chat.id, 'Хотите прикрепить файлы к сообщению?',
                             reply_markup=InlineKeyboard([['Да', 'yes_files'], ['Нет', 'no_files']]))
    else:
        bot.send_message(message.chat.id, 'Пришлите мне <b>текст</b> сообщения', parse_mode='html')
        bot.register_next_step_handler_by_chat_id(message.chat.id, message_for_admin)


def menu_keyboard():
    for each in ParentButton.objects.all():
        each.callback = translit(each.text)
        each.save()

    for each in GrandParentButton.objects.all():
        each.callback = translit(each.text)
        each.save()

    board = []
    for button in GrandParentButton.objects.all():
        board.append([button.name, button.callback[:64]])
    board.append(['Остались вопросы?', 'questions'])

    keyboard = InlineKeyboard(board)

    return keyboard


def respond(message):
    admin = Admin.objects.get(id=message.chat.id)
    message_ = MessageBot.objects.get(id=admin.message_on_respond)
    user = message_.user
    bot.send_message(user.user_id, f'Пришел ответ на Ваше сообщение:\n\n<i>{message_.text}</i>\n\n{message.text}',
                     parse_mode='html')
    bot.send_message(message.chat.id, 'Сообщение отправлено')


class Command(BaseCommand):
    def handle(self, *args, **options):
        global bot
        bot.polling(none_stop=True)


@bot.message_handler(commands=['help', 'start'])
def help_command(message):
    bot.send_message(message.chat.id, 'Этот бот призван облегчить общение родителей обучающихся с центром платных'
                                      ' услуг Инженерного Лицея НГТУ.\nНиже вы можете увидеть список возможных команд'
                                      ' с кратким описанием\n\n/help - посмотреть эту памятку\n/menu - главное меню\n')


@bot.message_handler(commands=['menu'])
def menu_command(message):
    if message.chat.id in (admin.id for admin in Admin.objects.all()):
        keyboard = InlineKeyboard([['Сообщения пользователей', 'user_messages'],
                                   ['Панель администратора', 'https://example.com']])

    else:
        if BotUser.objects.filter(user_id=message.chat.id) and Condition.objects.filter(user_id=message.chat.id):
            condition = Condition.objects.get(user=BotUser.objects.get(user_id=message.chat.id))
            condition.creating_message = False
            condition.save()
            bot.clear_step_handler_by_chat_id(message.chat.id)

        elif BotUser.objects.filter(user_id=message.chat.id) and not \
                Condition.objects.filter(user_id=message.chat.id):
            Condition(user_id=message.chat.id).save()
            bot.clear_step_handler_by_chat_id(message.chat.id)

        keyboard = menu_keyboard()

    bot.send_message(chat_id=message.chat.id, text='Главное меню:', parse_mode='html',
                     reply_markup=keyboard)


# processing files from the users
@bot.message_handler(content_types=['document', 'photo', 'video'], func=lambda message: Condition.objects.get(
    user=BotUser.objects.get(user_id=message.chat.id)).creating_message)
def doc_handler(message):
    user = BotUser.objects.get(user_id=message.chat.id)
    group_id = message.media_group_id
    file = ''
    if group_id:
        if MessageBot.objects.filter(user=user).last().media_group:
            message_ = MessageBot.objects.filter(user=user).last()
        else:
            message_ = MessageBot.objects.filter(user=user, media_group=group_id)
            if message_:
                message_ = message_[0]
            else:
                message_ = MessageBot.objects.filter(user=user, media_group=None).last()
                message_.media_group = group_id
    else:
        if MessageBot.objects.filter(user=user).last().media_group:
            message_ = MessageBot.objects.filter(user=user).last()
        else:
            message_ = MessageBot.objects.filter(user=user, media_group=None).last()

    if message.document:
        file = bot.get_file(message.document.file_id)
    elif message.photo:
        file = bot.get_file(message.json['photo'][-1]['file_id'])
    elif message.video:
        file = bot.get_file(message.video.file_id)

    extension = str(file.file_path).split('.')[-1]
    file_name = str(file.file_path).split('/')[1]
    file = bot.download_file(file.file_path)

    AttachmentBot(message_bot=message_, data=file, name=file_name, extension=extension).save()
    message_.save()

    bot.send_message(message.chat.id, f'Файл {file_name} отправлен',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


# GrandParentButton callbacks
@bot.callback_query_handler(
    func=lambda call: call.data in [button.callback for button in GrandParentButton.objects.all()])
def callback_buttons(call):
    button = list(
        filter(lambda button: button.callback == call.data, [button for button in GrandParentButton.objects.all()]))
    files = []
    if button[0].parent:
        for each in button[0].parent.all():
            each.callback = translit(each.text)[:64]
            each.save()
        buttons = [[button.name, button.callback[:64]] for button in button[0].parent.all()]
        buttons.append(['<- Назад', 'back'])

        keyboard = InlineKeyboard(buttons)
    else:
        keyboard = None

    if button[0].attachment:
        for file in button[0].attachment.all():
            files.append(open('djangoProject5/uploads/' + str(file), 'rb'))

        if len(files) > 10:
            raise FilesLimitExceeded

        try:
            bot.send_media_group(call.message.chat.id, media=[telebot.types.InputMediaDocument(file) for file in files])

            bot.send_message(call.message.chat.id, text=button[0].text,
                             reply_markup=keyboard, parse_mode='html')
        except Exception:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=button[0].text,
                                  parse_mode='html', reply_markup=keyboard)


# ParentButton callbacks
@bot.callback_query_handler(func=lambda call: call.data in [button.callback for button in ParentButton.objects.all()])
def callback_buttons(call):
    global keyboard
    button = list(
        filter(lambda button: button.callback == call.data, [button for button in ParentButton.objects.all()]))
    files = []
    if button[0].child:
        for each in button[0].child.all():
            each.callback = translit(each.text)[:64]
            each.save()
        buttons = [[button.name, button.callback[:64]] for button in button[0].child.all()]
        buttons.append([['<- Назад', button[0].grandparent.callback[:64]], ['Меню', 'menu']])

        keyboard = InlineKeyboard(buttons)

    if button[0].attachment:
        for file in button[0].attachment.all():
            files.append(open('djangoProject5/uploads/' + str(file), 'rb'))

        if len(files) > 10:
            raise FilesLimitExceeded
        try:
            bot.send_media_group(call.message.chat.id, media=[telebot.types.InputMediaDocument(file) for file in files])

            bot.send_message(call.message.chat.id, text=button[0].text,
                             reply_markup=keyboard, parse_mode='html')
        except Exception:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=button[0].text,
                                  parse_mode='html', reply_markup=keyboard)


# ChildButton callbacks
@bot.callback_query_handler(func=lambda call: call.data in [button.callback for button in ChildButton.objects.all()])
def c(call):
    button = list(filter(lambda button: button.callback == call.data, [button for button in ChildButton.objects.all()]))

    button[0].callback = translit(button[0].parent.text)[:64]
    button[0].save()
    buttons = [['<- Назад', button[0].parent.callback[:64]], ['Меню', 'menu']]
    keyboard = InlineKeyboard([buttons])
    files = []

    if button[0].attachment:
        for file in button[0].attachment.all():
            files.append(open('djangoProject5/uploads/' + str(file), 'rb'))

        if len(files) > 10:
            raise FilesLimitExceeded

        try:
            bot.send_media_group(call.message.chat.id, media=[telebot.types.InputMediaDocument(file) for file in files])
            bot.send_message(call.message.chat.id, text=button[0].text, reply_markup=keyboard, parse_mode='html',)
        except Exception:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=button[0].text,
                                  parse_mode='html', reply_markup=keyboard)


# static callbacks
@bot.callback_query_handler(func=lambda call: call.data in USER_CALLBACKS)
def user_callbacks_handler(call):
    if call.data in ['menu', 'back']:

        if BotUser.objects.filter(user_id=call.message.chat.id) and \
                Condition.objects.filter(user_id=call.message.chat.id):
            condition = Condition.objects.get(user=BotUser.objects.get(user_id=call.message.chat.id))
            condition.creating_message = False
            condition.save()
            bot.clear_step_handler_by_chat_id(call.message.chat.id)

        elif BotUser.objects.filter(user_id=call.message.chat.id) and not \
                Condition.objects.filter(user_id=call.message.chat.id):
            Condition(user_id=call.message.chat.id).save()
            bot.clear_step_handler_by_chat_id(call.message.chat.id)

        keyboard = menu_keyboard()

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Главное меню:',
                              reply_markup=keyboard,
                              parse_mode='html'
                              )

    elif call.data == 'questions':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Если у вас ещё остались вопросы, то вы можете связаться с руководителем центра плат'
                                   'ных услуг.\n<b>Науменко-Тарасова Алёна Леонидовна</b> \nПо телефону: <b>355-40-21</'
                                   'b>\nВ рабочие дни с <b>11:00-16:00</b>',
                              parse_mode='html',
                              reply_markup=InlineKeyboard([['Написать сообщение администратору', 'message'],
                                                           ['<-Назад', 'menu']]))

    elif call.data == 'message':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Пришлите мне текст сообщения',
                              parse_mode='html',
                              reply_markup=None)
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, message_for_admin)

    elif call.data == 'no_files':
        message_ = MessageBot.objects.filter(user=BotUser.objects.get(user_id=call.message.chat.id)).last()
        message_.media_group = 0
        message_.save()

        bot.answer_callback_query(call.id, 'Сообщение отправлено')

        for admin in Admin.objects.all():
            bot.send_message(admin.id, 'Вам пришло новое сообщение. Посмотреть список всех'
                                       ' сообщений можно с помощью команды /menu')

        keyboard = menu_keyboard()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Главное меню:',
                              parse_mode='html', reply_markup=keyboard)

    elif call.data == 'yes_files':
        for admin in Admin.objects.all():
            bot.send_message(admin.id, 'Вам пришло новое сообщение. Посмотреть список всех'
                                       ' сообщений можно с помощью команды /menu')

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Пришлите файлы. После отправки нажмите на команду /menu',
                              parse_mode='html',
                              reply_markup=None)

        condition = Condition.objects.get(user=BotUser.objects.get(user_id=call.message.chat.id))
        condition.creating_message = True
        condition.save()

    elif call.data == 'hide':
        bot.delete_message(call.message.chat.id, call.message.message_id)


# Admin menu in Telegram
@bot.callback_query_handler(func=lambda call: call.message.chat.id in (admin.id for admin in Admin.objects.all()))
def admin_callbacks_handler(call):
    if call.data == 'user_messages':
        messages_list = MessageBot.objects.all()
        if messages_list:
            length = len(messages_list)
            messages_list = [[f'Сообщение от {message.user.first_name}', f'{message.id} backward 0/{length}'] for
                             message in messages_list]
            if len(messages_list) > 4:
                messages_list = messages_list[0:4]
                messages_list.append(['вперед ->', f'forward 4/{length}'])
            keyboard = InlineKeyboard(messages_list)
            bot.send_message(call.message.chat.id, f'Выберите сообщение. Всего сообщений: {length}',
                             reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, 'У вас нет сообщений')

    elif len(call.data.split()) == 3:
        attachments = AttachmentBot.objects.filter(message_bot=MessageBot.objects.get(id=int(call.data.split()[0])))
        if attachments:
            bot.delete_message(call.message.chat.id, call.message.message_id)

            names = [attachment.name for attachment in attachments]

            for i in range(len(attachments)):
                bot.send_document(call.message.chat.id, attachments[i].data, visible_file_name=f'{names[i]}')
        bot.send_message(call.message.chat.id, f'Сообщение:\n\n'
                                               f'{MessageBot.objects.get(id=int(call.data.split()[0])).text}',
                         reply_markup=InlineKeyboard([[['<- Назад', f'{call.data.split()[1]} {call.data.split()[2]}'],
                                                       ['Ответить', f'respond {int(call.data.split()[0])}']]]),
                         parse_mode='html')

    elif 'forward' in call.data:
        from_ = int(call.data.split()[1].split('/')[0])
        length = int(call.data.split()[1].split('/')[1])
        messages_list = [[f'Сообщение от {message.user.first_name}', f'{message.id} {call.data}'] for message in
                         MessageBot.objects.all()]
        if length - from_ <= 4:
            buttons = [['<- назад', f'backward {from_ - 4}/{length}']]
            keyboard = InlineKeyboard(messages_list[from_:])
            keyboard.row(
                *[telebot.types.InlineKeyboardButton(button[0], callback_data=button[1]) for button in buttons])
        else:
            buttons = [['<- назад', f'backward {from_ - 4}/{length}'], ['вперед ->', f'forward {from_ + 4}/{length}']]
            keyboard = InlineKeyboard(messages_list[from_:from_ + 4])
            keyboard.row(
                *[telebot.types.InlineKeyboardButton(button[0], callback_data=button[1]) for button in buttons])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Выберите сообщение. Всего сообщений: {length}',
                              parse_mode='htm',
                              reply_markup=keyboard)

    elif 'backward' in call.data:
        from_ = int(call.data.split()[1].split('/')[0])
        length = int(call.data.split()[1].split('/')[1])
        messages_list = [[f'Сообщение от {message.user.first_name}', f'{message.id} {call.data}'] for message in
                         MessageBot.objects.all()]

        if length <= 4:
            keyboard = InlineKeyboard(messages_list)
        elif length - from_ <= 4:
            buttons = [['<- назад', f'backward {from_ - 4}/{length}']]
            keyboard = InlineKeyboard(messages_list[from_:])
            keyboard.row(
                *[telebot.types.InlineKeyboardButton(button[0], callback_data=button[1]) for button in buttons])
        elif from_ == 0:
            length = len(messages_list)
            if len(messages_list) > 4:
                messages_list = messages_list[0:4]
                messages_list.append(['вперед ->', f'forward 4/{length}'])
            keyboard = InlineKeyboard(messages_list)
        else:
            buttons = [['<- назад', f'backward {from_ - 4}/{length}'], ['вперед ->', f'forward {from_ + 4}/{length}']]
            keyboard = InlineKeyboard(messages_list[from_:from_ + 4])
            keyboard.row(
                *[telebot.types.InlineKeyboardButton(button[0], callback_data=button[1]) for button in buttons])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Выберите сообщение. Всего сообщений: {length}',
                              parse_mode='html',
                              reply_markup=keyboard)

    elif 'respond' in call.data:
        bot.send_message(call.message.chat.id, 'Отправьте мне текст сообщения')

        admin = Admin.objects.get(id=call.message.chat.id)
        admin.message_on_respond = int(call.data.split()[1])
        admin.save()

        bot.register_next_step_handler_by_chat_id(call.message.chat.id, respond)
