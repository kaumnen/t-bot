from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
import time

# import for NASA's APOD
from nasa_apod import Nasa_apod

# reading secret info
from configparser import ConfigParser

# read .ini file
config_object = ConfigParser()
config_object.read(".ini")

# get the data
tg_api = config_object["TELEGRAM_API"]
api_key = tg_api["api_key"]

updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def sending_message(context, update, message):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    time.sleep(3)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def waiting_writing(update, context, n):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    time.sleep(n)

# command functions
def start(update, context):
    sending_message(context, update, 'Hey there, I\'m t-bot\. \n\nWelcome\! \n\n'
                                                                    'Waiting for some phenomenal commands 😃')
    sending_message(context, update, 'Are you confused?  \'cuz I\'d be')
    sending_message(context, update, 'In case you are still confused, send me /help for more info.')


def help_command(update, context):
    sending_message(context, update, 'You thought I can just scream in chat? '
                                                                    'Ooh no no, pay attention:')
    sending_message(context, update, '1. Send /caps and '
                                    'write message you want me to repeat IN CAPS!')

    context.bot.send_animation(chat_id=update.effective_chat.id,
                               animation='https://media1.tenor.com/images/a954d1d5e35324dae774c5bfb8095cc6/tenor.gif')
    waiting_writing(update, context, 3)
    sending_message(context, update, '2. Send /nasa to me, and I will return NASA\'s '
                                                                    'Astronomy Picture Of the Day!')
    sending_message(context, update, 'For now, I can '
                                                                    'do '
                                                                    '/caps command when you mention me somewhere. Just '
                                                                    'write \'@awsmm_bot some_text\', replace '
                                                                    'some_text with your text, and hit that \'Caps\' '
                                                                    'button 😂')
    sending_message(context, update, 'Also, I will repeat'
                                                                    ' (in private chat) whatever you say to me that'
                                                                    ' ain\'t command. '
                                                                    'Remember that I don\'t have any them brains lol.'
                                                                    '\n\nIf you need short version of /help, '
                                                                    'send me /welp.')

def welp(update, context):
    sending_message(context, update, '/caps - returns same text CAPS-ED\n'
                                                                    '/nasa - returns NASA\'s APOD\n'
                                                                    '/help - returns help obviously\n'
                                                                    '/welp - this escalates quickly\n')


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    print(update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def nasa(update, context):
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=Nasa_apod().retrieve_picture_url())
        waiting_writing(update, context, 2)
        context.bot.send_message(chat_id=update.effective_chat.id, text=Nasa_apod().retrieve_picture_info())

        if Nasa_apod().retrieve_text_with_picture():
            waiting_writing(update, context, 5)
            context.bot.send_message(chat_id=update.effective_chat.id, text=Nasa_apod().retrieve_text_with_picture())
    except:
        sending_message(context, update, 'This service is not operational right now. Please try later.')


# inline command functions
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


# if user input non-existing command - MUST BE LAST ONE DEFINED
def unknown(update, context):
    sending_message(context, update, 'Sorry, I DON\'T UNDERSTAND THAT!')


# normal commands to dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help_command)
dispatcher.add_handler(help_handler)

welp_handler = CommandHandler('welp', welp)
dispatcher.add_handler(welp_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

nasa_apod_handler = CommandHandler('nasa', nasa)
dispatcher.add_handler(nasa_apod_handler)

# inline commands to dispatcher
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

# if user input non-existing command - MUST BE LAST ONE DEFINED
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# start
updater.start_polling()

# working until stop signal received (SIGINT)
updater.idle()
