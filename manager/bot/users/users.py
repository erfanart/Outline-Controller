from telegram import Update
from telegram.ext import ContextTypes
from manager.bot.front import Front
from manager.vpn import Keys
from manager.vpn.server import Server
from manager.setting import CONFIG
from .admin import Admin

class Users(Front):

    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)
        self.admin = Admin()
    
    async def check_user(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("Checking User : " , update.effective_user.id)
        try : 
            chatid = update.effective_user.id
            if chatid == 647340579:
                return "Is_Admin"
                # await self.admin_panel(update=update,context=context)
        except Exception as e :
            print(e)
            print(update.message)
