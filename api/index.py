from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel

from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

TOKEN = "6153368129:AAGOrqF2egWHFwgBC02kq3icGhzCaT1gzWk"

app = FastAPI()

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

def start(update, context):
    user_id = update.message.from_user.id

    markup = InlineKeyboardMarkup()
    button_amharic = InlineKeyboardButton(text='አማርኛ', callback_data='amharic')
    button_english = InlineKeyboardButton(text='English', callback_data='english')
    markup.add(button_amharic, button_english)

    context.bot.send_message(
        chat_id=user_id,
        text="Please choose your language. \nእባክዎ ቋንቋዎን ይምረጡ።",
        reply_markup=markup
    )

def register_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    # Method 1
    bot = Bot(token=TOKEN)
    update = Update.de_json(webhook_data.__dict__, bot) # convert the Telegram Webhook class to dictionary using __dict__ dunder method
    dispatcher = Dispatcher(bot, None, workers=4)
    register_handlers(dispatcher)

    # handle webhook request
    dispatcher.process_update(update)

    # Method 2
    # you can just handle the webhook request here without using python-telegram-bot
    # if webhook_data.message:
    #     if webhook_data.message.text == '/start':
    #         send_message(webhook_data.message.chat.id, 'Hello World')
    
    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello Worldoch"}
