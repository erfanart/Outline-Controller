
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes
import time
from manager import vpn
from manager.bot.server_side.manage_key import *
from manager.bot.users import Users

class Server_Side(Manage_Key):
    
    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)
        self.users = Users()

    async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        await user.start(update=update,context=context)

        

    async def cancel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id= update.effective_chat.id,text = " ختم لغو شد جهت شروع مجدد روی گزینه ی زیر کلیک کنید",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="منو اصلی",callback_data="/start")]]))
        await self.start(update=update,context=context)
        print("cancelling done")
        return ConversationHandler.END
    
    async def update_server(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        vpn_server = vpn
        vpn_server.update()
        await self.send_message(update=update,context=context,text="اپدیت انجام شد")
        time.sleep(2)
        await self.start(update=update,context=context)


