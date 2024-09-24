from telegram import Update
from telegram.ext import ConversationHandler,ContextTypes
from manager.bot.front import Front
from manager.vpn.server import Server
from manager.setting import *
from manager.vpn import *
from manager import vpn
import asyncio 
from manager.bot.users import Users



class Manage_Key(Front):
    
    def __init__(self):
        self.URL = CONFIG['servers']['url']
        self.PASS = CONFIG['servers']['pass'] 
        self.server = Server(self.URL,self.PASS)
        self.keys = Keys(self.server)
        self.users = Users()


    async def check_key_detail(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        if hasattr(user,"check_key_detail"):
            return await user.check_key_detail(update=update,context=context)
        else:
            btn = {
            "start":"بازگشت"
            }
            but = await self.make_inline_key(btn)
            text = "شما به این بخش دسترسی ندارید "
            await self.send_message(update=update,context=context,text=text,key=but)


    async def check_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        if hasattr(user,"check_key"):
            return await user.check_key(update=update,context=context)
        else:
            btn = {
            "start":"بازگشت"
            }
            but = await self.make_inline_key(btn)
            text = "شما به این بخش دسترسی ندارید "
            await self.send_message(update=update,context=context,text=text,key=but)
        

    async def update_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        if hasattr(user,"update_key"):
            return await user.update_key(update=update,context=context)
        else:
            btn = {
            "start":"بازگشت"
            }
            but = await self.make_inline_key(btn)
            text = "شما به این بخش دسترسی ندارید "
            await self.send_message(update=update,context=context,text=text,key=but)
            
            
            
    async def action(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        if hasattr(user,"action"):
            return await user.action(update=update,context=context)
        else:
            btn = {
            "start":"بازگشت"
            }
            but = await self.make_inline_key(btn)
            text = "شما به این بخش دسترسی ندارید "
            await self.send_message(update=update,context=context,text=text,key=but)



    async def get_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        if hasattr(user,"get_key"):
            return await user.get_key(update=update,context=context)
        else:
            btn = {
            "start":"بازگشت"
            }
            but = await self.make_inline_key(btn)
            text = "شما به این بخش دسترسی ندارید "
            await self.send_message(update=update,context=context,text=text,key=but)
        
    async def nonupdate_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        UserRole = await self.users.check_user(update=update,context=context)
        user = getattr(self.users,str.lower(UserRole))
        if hasattr(user,"nonupdate_key"):
            return await user.nonupdate_key(update=update,context=context)
        else:
            btn = {
            "start":"بازگشت"
            }
            but = await self.make_inline_key(btn)
            text = "شما به این بخش دسترسی ندارید "
            await self.send_message(update=update,context=context,text=text,key=but)