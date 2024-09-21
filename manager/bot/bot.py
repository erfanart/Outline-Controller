
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler,ConversationHandler,BaseHandler,JobQueue , filters, ContextTypes,Updater,CallbackContext, CallbackQueryHandler
from telegram.warnings import PTBUserWarning
import asyncio 
from manager import vpn
from manager.vpn import *
from manager.setting import *
from manager.bot.client_side import *
from manager.bot.server_side import *
from warnings import filterwarnings
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

class Bot(Server_Side):
    def __init__(self):
        super().__init__()




    async def makeapp(self,TOKEN,URL):
        try:
            app = Application.builder().base_url(URL).token(TOKEN).build()
            app.add_handlers([

                MessageHandler(filters.Text(["/start","start","شروع"]) ,self.start),
                CallbackQueryHandler(self.start,"start"),
                CallbackQueryHandler(self.update_server,"update_server"),
                CallbackQueryHandler(self.nonupdate_key,"nonupdate_key"),

                ConversationHandler(
                    entry_points=[CallbackQueryHandler(self.check_key,"check")],
                    states={
                        "check":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.check_key),CallbackQueryHandler(self.check_key)],
                        "details":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.check_key_detail),CallbackQueryHandler(self.check_key_detail)],
                        # "change":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,action),CallbackQueryHandler(action)]
                    },
                    fallbacks=[MessageHandler(filters.Text("/cancel"), self.cancel),CallbackQueryHandler(self.cancel,"cancel")],
                    ),

                ConversationHandler(
                entry_points= [CallbackQueryHandler(self.update_key,"update_key")],
                states={
                    "update_key" : [MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.update_key),CallbackQueryHandler(self.update_key)],
                    "get key": [MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.get_key),CallbackQueryHandler(self.get_key)],
                    "action":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.action),CallbackQueryHandler(self.action)]
                },
                fallbacks=[MessageHandler(filters.Text("/cancel"), self.cancel),CallbackQueryHandler(self.cancel,"cancel")],
                ),


            ])
            app.add_error_handler(self.error)
            print('polling...')
            async with  app:
                await app.initialize()
                await app.start()
                await app.updater.start_polling()
                try:
                    await asyncio.Event().wait()
                    await app.stop
                except:
                    await app.stop
        except Exception as e:
            print(e)




