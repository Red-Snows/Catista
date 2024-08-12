from telebot import TeleBot,types
import json
import requests
     
bot = TeleBot('')#Telegram Bot Token Here :)
global started 
started = []

@bot.message_handler(commands=['start'])
def welcome(message: types.Message):
    name = message.from_user.first_name
    text = f'سلام {name} عزیز لینک پست اینستایی که میخوای رو بفرست تا ویدیو رو برات ارسال کنم'
    bot.reply_to(message,text)
    started.append(f"{message.chat.id}")
    with open('UserStarted.txt','w') as file:
        json.dump(started,file)

@bot.message_handler(commands=['about'])
def about(message:types.Message):
    channel = types.InlineKeyboardButton('کانال کتیستا',url='Channel Username')
    btn = types.InlineKeyboardMarkup()
    btn.add(channel)
    aboutMessage = 'ربات کتیستا یک ربات دانلود از اینستاگرام با سرعت زیاده که میتونی به صورت نامحدود ازش استفاده کنی\nنکته جالب اینه که نیاز به جوین اجباری رو مخ نداری\n\nBy : @NeyXy'
    bot.reply_to(message,aboutMessage,reply_markup=btn)

@bot.message_handler(func=lambda m:True)
def sendVideo(message:types.Message):
    if message.text.startswith('https://www.instagram.com'):
        link = message.text[12:]
        link = f"www.dd{link}"
        channel = types.InlineKeyboardButton('کانال کتیستا',url='Channel Username')
        report = types.InlineKeyboardButton('گزارش باگ',callback_data='report')
        btn = types.InlineKeyboardMarkup(row_width=2)
        btn.add(channel,report)
        bot.send_message(message.chat.id, f'<a href="{link}">⁪</a> خدمت شما🐈‍⬛', parse_mode='HTML',reply_markup=btn)
    else:
        bot.reply_to(message,'مثل اینکه پیامی که دادی لینک اینستاگرامی نیست :(')

@bot.callback_query_handler(func=lambda call:True)
def GetCall(call:types.CallbackQuery):
    if call.data == 'report':
        bot.answer_callback_query(call.id,'شما در حال گزارش باگ هستید')
        reportMessage = bot.send_message(call.message.chat.id,'دلیل گزارش خودتون رو بنویسید')
        bot.register_next_step_handler(reportMessage,get_report)

    elif call.data.startswith('file_'):
        try:
            pass
        except Exception as e:
            report = types.InlineKeyboardButton('گزارش',callback_data=f'filerep_{e}')
            repbtn = types.InlineKeyboardMarkup()
            repbtn.add(report)
            bot.send_message(call.message.chat.id,'مشکلی پیش اومده',reply_markup=repbtn)

    elif call.data.startswith('filerep_'):
        bot.send_message(call.message.chat.id,call.data)
        bot.send_message(call.message.chat.id,'گزارش شما ارسال شد')
def get_report(message:types.Message):
    text = message.text
    bot.send_message(6826370418,f"{text}\n\n chat id : {message.chat.id}\n\n id = {message.from_user.username}")
    bot.reply_to(message,'گزارش شما با موفقیت ثبت شد ممنون از گزارش شما')

try:
    with open('UserStarted.txt','r') as file:
        started = json.load(file)
except:
    pass
print('bot started')
bot.infinity_polling()
