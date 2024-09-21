
from telegram import Update
from telegram.ext import ContextTypes
import time
from manager import vpn
from manager.bot.server_side.manage_key import *
from manager.bot.server_side.manage_user import *

class Server_Side(Manage_Key,Manage_User):
    
    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)


    async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        # text: str = update.message.text
        await self.check_user(update=update,context=context)



    async def update_server(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        vpn_server = vpn
        vpn_server.update()
        await self.send_message(update=update,context=context,text="اپدیت انجام شد")
        time.sleep(2)
        await self.start(update=update,context=context)


