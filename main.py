from telebot import *
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
import pdfplumber

load_dotenv()

API_KEY = os.getenv("API_KEY") or ""
bot = telebot.TeleBot(API_KEY)
lang_list = "en/ru/es/fr/de"
file_name = ''
text = ''
text_size = None
text_size_limit = 3000
text_split = None
done = False


@bot.message_handler(commands=['start', 'help'])
def send_wellcome(message):
    bot.reply_to(message, 'Sup?')
    doc = open('images\\Cat03.jpg', 'rb')
    bot.send_photo(message.chat.id, doc)
    bot.send_message(message.chat.id, "Send me some PDFs and I'll voice them over to an MP3 file!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Sorry, mate, but I only understand PDFs yet \U0001F917')
    bot.send_message(message.chat.id, "C'mon, try me!")


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    global file_name
    file_name = file_info.file_path.split('/')[1].lower()
    if '.pdf' in file_name:
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_KEY, file_info.file_path))
        with open('downloads\\{0}'.format(file_name), 'wb') as file_new:
            file_new.write(file.content)

        with pdfplumber.PDF(open(file='downloads\\{0}'.format(file_name), mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]

        global text
        global text_size
        global text_split
        text = ''.join(pages)
        text = text.replace('\n', '')
        text_size = len(text)
        text_split = [text[i:i + text_size_limit] for i in range(0, len(text), text_size_limit)]

        if text_size > text_size_limit:
            bot.send_message(message.chat.id, f'Document is too big and will be split to {len(text_split)} parts')
            choice = bot.send_message(message.chat.id, 'Proceed? (Y/N)')
            bot.register_next_step_handler(choice, choice_choice)
        else:
            bot.reply_to(message, "Great, what language do you prefer?")
            lang = bot.send_message(message.chat.id, lang_list)
            bot.register_next_step_handler(lang, lang_choice)
    else:
        bot.reply_to(message, 'This is not a PDF')


def choice_choice(message):
    if message.text.lower() in ['yes', 'y', 'yep', 'ye']:
        bot.reply_to(message, "Great, what language do you prefer?")
        lang = bot.send_message(message.chat.id, lang_list)
        bot.register_next_step_handler(lang, lang_choice)
    elif message.text.lower() in ['n', 'no', 'nope', 'nah']:
        bot.send_message(message.chat.id, 'Ok, no problem :)')
        return
    else:
        lang = bot.send_message(message.chat.id, 'Would you like to split the result? (Y/N)')
        bot.register_next_step_handler(lang, choice_choice)
        return


def lang_choice(message):
    if message.text.lower() not in lang_list:
        lang = bot.send_message(message.chat.id, 'Please choose supported language!')
        bot.send_message(message.chat.id, lang_list)
        bot.register_next_step_handler(lang, lang_choice)
        return
    else:
        if text_size > text_size_limit:
            doc_processor(message)
        else:
            doc_processing(message)


def doc_processing(message):
    global file_name
    global done
    global text
    done = False
    while not done:
        process = bot.send_message(message.chat.id, 'Processing file...')
        bot.register_next_step_handler(process, not_done)
        my_audio = gTTS(text=text, lang=message.text.lower(), slow=False)
        my_audio.save('downloads\\Document.mp3')
        print(' [+] Document.mp3 has been successfully saved!')
        bot.send_message(message.chat.id, 'Done!')
        bot.send_message(message.chat.id, 'Sending MP3 file...')
        with open('downloads\\Document.mp3', 'rb') as processed_file:
            bot.send_document(message.chat.id, processed_file)
        done = True


def doc_processor(message):
    global text_split
    number = 1
    process = bot.send_message(message.chat.id, 'Processing file...')
    bot.register_next_step_handler(process, not_done)
    for i in text_split:
        my_audio = gTTS(text=i, lang=message.text.lower(), slow=False)
        my_audio.save(f'downloads\\Part{number}.mp3')
        print(f' [+] Part{number}.mp3 has been successfully saved!')
        with open(f'downloads\\Part{number}.mp3', 'rb') as processed_file:
            bot.send_document(message.chat.id, processed_file)
        number += 1
    bot.send_message(message.chat.id, 'Done!')


def not_done(message):
    global done
    if not done:
        process = bot.send_message(message.chat.id, "Sorry, still working with your file, please wait.")
        bot.register_next_step_handler(process, not_done)
    return


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    bot.reply_to(message, 'Nice photo, mate, but I only work with PDFs')
    bot.send_message(message.chat.id, "C'mon, try me!")


bot.infinity_polling()
