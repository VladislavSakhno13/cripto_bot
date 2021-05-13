import telebot
import requests
import json
import config
from telebot import types
bot = telebot.TeleBot(config.TOKEN)

def get_binance_price(pair):
    list_pair = pair
    getprice = requests.get('https://api.binance.com/api/v1/klines?symbol='+list_pair.upper()+'&interval=1m&limit=1')
    return float(getprice.json()[0][4])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Добро пожаловть в бот. Напишите пару и цену (BTCUSDT 51.346) и мы оповестим вас когда цена будет достигнута')

@bot.message_handler(content_types=['text'])
def send_price(message):
    list_pair = message.text.split()
    getprice = requests.get('https://api.binance.com/api/v1/klines?symbol='+list_pair[0].upper()+'&interval=1m&limit=1')
    if(isinstance(getprice.json(),list)):

        enter_price = get_binance_price(list_pair[0])#Цена на момент входа
        print('Цена на момент входа - '+str(enter_price))
        need_price = float(list_pair[1]) #цена при достижении которой придет оповещение
        print('цена при достижении которой придет оповещение - '+str(need_price))
        if(need_price>enter_price):#если нужная цена выше
            while True:
                price_point = get_binance_price(list_pair[0])#текущая цена
                if(need_price>=price_point):
                    bot.send_message(message.chat.id,"Цена достигнута - +"+list_pair[0]+"="+str(get_binance_price(list_pair[0])))
                    break
        if(need_price<enter_price):#если нужная цена ниже
             while True:
                price_point = get_binance_price(list_pair[0])#текущая цена
                if(need_price<=price_point):
                    print("нужная цена - "+str(need_price))
                    print("текущая цена - "+str(price_point))
                    bot.send_message(message.chat.id,"Цена достигнута - -"+str(list_pair[0])+"="+str(get_binance_price(list_pair[0])))
                    break
    else:
        bot.send_message(message.chat.id,"Введенно не коректное сообщение")

bot.polling()