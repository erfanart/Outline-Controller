
from telegram import Update
from telegram.ext import ContextTypes
import time
from manager import vpn
from manager.bot.server_side.manage_key import *


class Server_Side(Manage_Key):
    
    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)

    async def update_server(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        vpn_server = vpn
        vpn_server.update()
        await self.send_message(update=update,context=context,text="اپدیت انجام شد")
        time.sleep(2)
        await self.start(update=update,context=context)


