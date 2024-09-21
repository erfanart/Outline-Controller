from telegram import Update
from telegram.ext import ConversationHandler,ContextTypes
from manager.bot.client_side import *
from manager.vpn.server import Server
from manager.setting import *
from manager.vpn import *
from manager import vpn


class Manage_User:

    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)
    
    async def check_user(self):
        pass