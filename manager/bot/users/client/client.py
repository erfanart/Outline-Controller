from telegram import Update
from telegram.ext import ContextTypes
from manager.bot.front import Front
from manager.setting import *
from manager.vpn import *
 
class Client(Front):
    
    async def panel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        text: str = "انتخاب کنید"
        btn = {
            "update_key":"تغییر کلید",
            "check":"بررسی وضعیت کلید",
            "nonupdate_key":"نمایش کلید های غیر فعال",
            "all":"نمایش کلید های من"
        }
        but = await self.make_inline_key(btn)
        await self.send_message(update=update,context=context,text=text,key=but)