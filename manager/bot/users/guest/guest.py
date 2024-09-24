from telegram import Update
from telegram.ext import ContextTypes
from manager.bot.front import Front
from manager.setting import *
from manager.vpn import *
 
class Guest(Front):
    async def panel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        text: str = """
سلام به ربات ما خوش آمدید
برای فعال سازی پنل مدیریت ، 
کلید خود را اضافه کنید تا پیامی به شماره تلفن منحصر به مدیر کلید ارسال شود و پس از آن کد ارسال شده را وارد کنید تا مراحل احراز هویت تکمیل گردد
        """
        btn = {
            "authenticate":"ارسال کلید",
        }
        but = await self.make_inline_key(btn)
        await self.send_message(update=update,context=context,text=text,key=but)