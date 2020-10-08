from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
import time

# import for NASA's APOD
from apis.nasa_apod import Nasa_apod

# responsible for quotes
from apis.random_quote import Quote

# responsible for cat pictures and gifs
from apis.random_cat_picture import Cats

# responsible for dog pictures
from apis.random_dog_picture import Dogs

# url shortener
from apis.url_shortener import short_url

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


def sending_message(update, context, message):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    time.sleep(2)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def waiting_writing(update, context, n):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    time.sleep(n)


# command functions
def start(update, context):
    sending_message(update, context, 'Hey there, I\'m t-bot\. \n\nWelcome\! \n\n'
                                     'Waiting for some phenomenal commands 😃')
    sending_message(update, context, 'Are you confused?  \'cuz I\'d be')
    sending_message(update, context, 'In case you are still confused, send me /help for more info.')


def help_command(update, context):
    sending_message(update, context, 'You thought I can just scream in chat? '
                                     'Ooh no no, pay attention:')
    sending_message(update, context, '1. Send /caps and '
                                     'write message you want me to repeat IN CAPS!')
    time.sleep(3)
    context.bot.send_animation(chat_id=update.effective_chat.id,
                               animation='https://media1.tenor.com/images/a954d1d5e35324dae774c5bfb8095cc6/tenor.gif')
    waiting_writing(update, context, 3)
    sending_message(update, context, '2. Send /url [URL] to me, and I will return shortened one '
                                     '(if you have reealy long url 😁).'
                                     '\nExclude \'https://www.\'!\ne.g. /url t.me/awsmm_bot')
    sending_message(update, context, '3. Send /nasa to me, and I will return NASA\'s '
                                     'Astronomy Picture Of the Day!')
    sending_message(update, context, '4. Send /quote to me, and I will return awesome quote for you!')
    sending_message(update, context, '5. Send /cat or /catgif to me, and I will return either cat\'s '
                                     'picture or gif. Meow!')
    sending_message(update, context, '6. Send /dogo to me, and I will send you great dog picture. Woof!')
    sending_message(update, context, 'For now, I can '
                                     'do '
                                     '/caps command when you mention me somewhere. Just '
                                     'write \'@awsmm_bot some_text\', replace '
                                     'some_text with your text, and hit that \'Caps\' '
                                     'button 😂')
    sending_message(update, context, 'Also, I will repeat'
                                     ' (in private chat) whatever you say to me that'
                                     ' ain\'t command. '
                                     'Remember that I don\'t have any them brains lol.'
                                     '\n\nIf you need short version of /help, '
                                     'send me /welp.')


def welp(update, context):
    sending_message(update, context, '/caps - returns same text CAPS-ED\n'
                                     '/url [URL] - returns shortened url, EXCLUDE https://www.\n'
                                     '/nasa - returns NASA\'s APOD\n'
                                     '/quote - returns great quote from internet\n'
                                     '/cat - returns cat picture\n'
                                     '/catgif - returns cat gif\n'
                                     '/dogo - returns dog picture\n'
                                     '/help - returns help obviously\n'
                                     '/welp - this escalates quickly\n')


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    print(context.args[0])
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def url_shortener(update, context):
    # if there is url passed after /url
    if context.args:
        url_provided = context.args[0]
        final_url = short_url(url_provided)

        if final_url:

            if len(final_url) > len(url_provided):
                sending_message(update, context, f'Well your link is shorter.. 😂\n'
                                                 f'However, here is \'shortened\' one: {final_url}')
            elif len(final_url) < len(url_provided):
                sending_message(update, context, f'My link is shorted for exactly '
                                                 f'{abs(len(final_url) - len(url_provided))} '
                                                 f'characters 😎\nHere you go: {final_url}')

            else:
                sending_message(update, context, f'Lengths are same! Your same-length url:\n {final_url}')

        else:
            sending_message(update, context, 'Either your url is too long, or my friends out'
                                             ' there are on quick vacation. Please try later!')

    else:
        sending_message(update, context, 'Please use command as intended.\n\n/url [URL]  ( EXCLUDE https://www. )')


def nasa(update, context):
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=Nasa_apod().retrieve_picture_url())
        waiting_writing(update, context, 2)
        context.bot.send_message(chat_id=update.effective_chat.id, text=Nasa_apod().retrieve_picture_info())

        if Nasa_apod().retrieve_text_with_picture():
            waiting_writing(update, context, 5)
            context.bot.send_message(chat_id=update.effective_chat.id, text=Nasa_apod().retrieve_text_with_picture())
    except:
        sending_message(update, context, 'This service is not operational right now. Please try later.')


def quote(update, context):
    sending_message(update, context, Quote().quote_msg())


def cat_picture(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=Cats().cat_url())


def cat_gif(update, context):
    context.bot.send_animation(chat_id=update.effective_chat.id,
                               animation=Cats().cat_gif_url())


def dog_picture(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=Dogs().dog_url())


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
    sending_message(update, context, 'Sorry, I DON\'T UNDERSTAND THAT!')


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

url_shortener_handler = CommandHandler('url', url_shortener)
dispatcher.add_handler(url_shortener_handler)

nasa_apod_handler = CommandHandler('nasa', nasa)
dispatcher.add_handler(nasa_apod_handler)

quote_handler = CommandHandler('quote', quote)
dispatcher.add_handler(quote_handler)

cat_picture_handler = CommandHandler('cat', cat_picture)
dispatcher.add_handler(cat_picture_handler)

cat_gif_handler = CommandHandler('catgif', cat_gif)
dispatcher.add_handler(cat_gif_handler)

dog_picture_handler = CommandHandler('dogo', dog_picture)
dispatcher.add_handler(dog_picture_handler)

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
