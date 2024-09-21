from typing import Final
from telegram import Update,Bot,KeyboardButton,ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler,ConversationHandler,BaseHandler,JobQueue , filters, ContextTypes,Updater,CallbackContext, CallbackQueryHandler
import asyncio 

class Cient_Side:

    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} Cussed Error {context.error}')


    async def cancel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        # await context.bot.send_message(chat_id= update.effective_chat.id,text = " ختم لغو شد جهت شروع مجدد روی گزینه ی زیر کلیک کنید",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="منو اصلی",callback_data="/start")]]))
        # await self.start(update=update,context=context)
        print("cancelling done")
        return ConversationHandler.END


    async def remove_msg(self,context: ContextTypes.DEFAULT_TYPE):
        JOB= context.job
        await context.bot.delete_message(
            chat_id = JOB.chat_id,
            message_id= JOB.data

         )
  


    async def send_message(self,update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = "هیچی نوشته نشده",key =None):
        query = update.callback_query
        KEY = key
        try:
            await query.edit_message_text(
                text= text,
                reply_markup=KEY,
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id= update.effective_chat.id,
                text = text,
                reply_markup= KEY, 
            )
            print(e)


    async def make_inline_key(self,BUTTONS):
        markup = []
        if BUTTONS:
            for button_id, button_text in BUTTONS.items():
                markup.append([InlineKeyboardButton(text=button_text, callback_data=f'{button_id}')])
        return InlineKeyboardMarkup(markup)      
    

    async def make_key(self,BUTTONS, place=None):
        markup = []
        if BUTTONS:
            for button_text in BUTTONS:
                markup.append([KeyboardButton(text=button_text)])
        return ReplyKeyboardMarkup(keyboard = markup,one_time_keyboard = True,input_field_placeholder = place)
