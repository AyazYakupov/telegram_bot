import telebot
import os
import validators
from selenium import webdriver
import configparser

FILE_INI = 'config.ini'
config = configparser.RawConfigParser()
config.read(FILE_INI)

bot = telebot.TeleBot(config.get('TELEGA', 'token'), threaded=False)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')


@bot.message_handler(commands=['start'])
def hello_user(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.username + '!')


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id,
                     'To get screenshot of webpage use command /getpng.\nExample: /getpng https://www.google.com')


@bot.message_handler(commands=['getpng'])
def get_screenshot(message):
    uid = message.chat.id
    url = ""
    try:
        url = message.text.split(' ')[1]
    except IndexError:
        bot.send_message(uid, 'You habe not entered URL!')
        return
    if not validators.url(url):
        bot.send_message(uid, 'URL is invalid!')
    else:
        photo_path = str(uid) + '.png'
        driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/lib/chromium-browser/chromedriver')
        driver.set_window_size(1280, 720)
        driver.get(url)
        driver.save_screenshot(photo_path)
        bot.send_photo(uid, photo=open(photo_path, 'rb'))
        driver.quit()
        os.remove(photo_path)


if __name__ == '__main__':
    bot.delete_webhook()
    bot.infinity_polling()
