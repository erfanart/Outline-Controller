from telegram import Update
from telegram.ext import ConversationHandler,ContextTypes
from manager.bot.client_side import *
from manager.vpn.server import Server
from manager.setting import *
from manager.vpn import *
from manager import vpn
import asyncio 


class Manage_User(Cient_Side):

    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)
    
    async def check_user(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        # print(update.message.chat_id)
        try : 
            chatid = update.message.chat_id
            if chatid == 647340579:
                await self.admin_panel(update=update,context=context)
        except Exception as e :
            print(e)
            print(update.message)
        

    async def admin_panel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        text: str = "انتخاب کنید"
        btn = {
            "update_server":"بروز رسانی کلید ها",
            "update_key":"تغییر کلید",
            "check":"بررسی وضعیت کلید",
            "nonupdate_key":"نمایش کلید های غیر فعال",
            "all":"نمایش کلید های من"

        }
        but = await self.make_inline_key(btn)
        await self.send_message(update=update,context=context,text=text,key=but)
    