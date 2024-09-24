from telegram import Update
from telegram.ext import ContextTypes
from manager.bot.client_side import *
from manager.setting import *
from manager.vpn import *
 
class Admin(Cient_Side):
    
    async def panel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        # return "cancel"
