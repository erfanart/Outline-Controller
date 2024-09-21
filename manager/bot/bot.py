
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler,ConversationHandler,BaseHandler,JobQueue , filters, ContextTypes,Updater,CallbackContext, CallbackQueryHandler
from telegram.warnings import PTBUserWarning
import asyncio 
from manager import vpn
from manager.vpn import *
from manager.setting import *
from manager.bot.client_side import *
from manager.bot.server_side import *
from warnings import filterwarnings
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

class Bot(Server_Side):
    def __init__(self):
        self.bots = CONFIG['bots']





    async def update_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            query = update.callback_query.data
            print("update_key func resived:",query)
            if query == "return":
                await self.start(update=update,context=context)
                return ConversationHandler.END
                # await cancel(update=update,context=context)
            elif query=="rechoose":
                but={
                    "expire":"مشاهده ی کلید های غیر فعال",
                    "return"  : "بازگشت"
                }
                btn = await self.make_inline_key(but)
                await self.send_message(update=update,context=context,text="مجددا ایدی کلید خود را مشخص کنید  برای",key=btn)
                # await get_value(update=update,context=context)
                return "get key"
            else:
                but={
                    "expire":"مشاهده ی کلید های غیر فعال",
                    "return"  : "بازگشت"
                }
                btn = await self.make_inline_key(but)
                await self.send_message(update=update,context=context,text="ایدی کلید خود را مشخص کنید  برای",key=btn)
                return "get key"
        except Exception as e:
                print("Acvtive Error :",e)
                return "get key"


    async def get_value(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            query = update.callback_query.data
            print(f"get_value qery resived:",query)
            if query == "expire" or query == "rechoose":
                txt = await self.expired_key()
                btn ={
                    "back":"بازگشت",
                    "return":"بازگشت به منوی اصلی",
                }
                btn = await self.make_inline_key(btn)
                await self.send_message(update=update,context=context,text=txt,key=btn)
            elif query == "return":
                await self.start(update=update,context=context)
                return ConversationHandler.END
            else:
                print("else of get value:",query)
                await self.update_key(update=update,context=context)
            # key.db.info(mode="status",table="keys",value="limited")
        except Exception as e:
            print("get_value func first exception :",e)
            text: str = update.message.text
            try:
                int(text)
                context.user_data["key_id"] = text
                print("id detected")
                await self.action(update=update,context=context)
                return "action"
            except Exception as e:
                print("get_value func second exception :",e)
                btn ={
                    "back":"بازگشت"
                }
                btn = await self.make_inline_key(btn)
                await self.send_message(update=update,context=context,text="لطفا عدد وارد کنید",key=btn)    
            print(text)


    async def nonupdate_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        txt = await self.expired_key()
        btn ={
            "start":"بازگشت به منوی اصلی"
        }
        btn = await self.make_inline_key(btn)
        await self.send_message(update=update,context=context,text=txt,key=btn)





    async def action(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            query = update.callback_query.data 
            print("action function recived:" , query)
            if query == "rechoose":
                await self.update_key(update=update,context=context)
                return "get key"
            elif query == "limit":
                btn ={
                    "back":"بازگشت"
                }
                btn = await self.make_inline_key(btn)
                context.user_data['method'] = "limit"
                await self.send_message(update=update,context=context,text="حجم مورد نظر خود را بر اساس گیگ وارد کنید",key=btn)
            elif query == "date":
                btn ={
                    "back":"بازگشت"
                }
                btn = await self.make_inline_key(btn)
                await self.send_message(update=update,context=context,text="زمان مورد نظر خود را بر اساس روز وارد کنید",key=btn)  
                context.user_data['method'] = "date"          
            else:
                btn ={
                    "limit":"تغییر حجم",
                    "date":"تغییر تاریخ انقضا",
                    "rechoose":"بازگشت",
                }
                btn = await self.make_inline_key(btn)
                await self.send_message(update=update,context=context,text="لطفا نوع عملیات خود را مشخص کنید",key=btn)    
        except Exception as e:
            print("action function First exseption: ", e)
            try:
                key_id = context.user_data["key_id"]
                method = context.user_data["method"] 
                if method == "date":             
                    try:
                        k = self.keys.vpndb.info("key_id","keys",key_id)
                        text = int(update.message.text)
                        self.keys.vpndb.update(key=k,method="date",unit=text)
                        context.user_data["key_id"] = ""
                        context.user_data["method"]  = ""
                        vpn.update()
                        await self.send_message(update=update,context=context,text="عملیات با موفقیت انجام شد")
                        await self.start(update=update,context=context)
                        return ConversationHandler.END
                    except Exception as e:
                        print("action function Thired exseption: ", e)
                        await self.send_message(update=update,context=context,text=f"خطا در {e}")
                        await self.start(update=update,context=context)
                        return ConversationHandler.END
                elif method == "limit":

                    try:
                        k = self.keys.vpndb.info("key_id","keys",key_id)
                        text = int(update.message.text)
                        context.user_data["key_id"] = ""
                        context.user_data["method"]  = ""
                        self.keys.vpndb.update(key=k,method="limit",unit=text)
                        vpn.update()
                        await self.send_message(update=update,context=context,text="عملیات با موفقیت انجام شد")
                        await self.start(update=update,context=context)
                        return ConversationHandler.END
                    except Exception as e:
                        print("action function Thired exseption: ", e)
                        await self.send_message(update=update,context=context,text=f"خطا در {e}")
                        await self.start(update=update,context=context)
                        return ConversationHandler.END
                else:
                    btn ={
                        "limit":"تغییر حجم",
                        "date":"تغییر تاریخ انقضا",
                        "rechoose":"بازگشت",
                    }
                    btn = await self.make_inline_key(btn)
                    await self.send_message(update=update,context=context,text="لطفا نوع عملیات خود را مشخص کنید",key=btn)   
            except Exception as e:
                print("action function seccond exseption: ", e)
                btn ={
                    "limit":"تغییر حجم",
                    "date":"تغییر تاریخ انقضا",
                    "rechoose":"بازگشت",
                }
                btn = await self.make_inline_key(btn)
                await self.send_message(update=update,context=context,text="لطفا نوع عملیات خود را مشخص کنید",key=btn) 

    ###################Ckeck Key Function



    async def makeapp(self,TOKEN,URL):
        try:
            app = Application.builder().base_url(URL).token(TOKEN).build()
            app.add_handlers([

                MessageHandler(filters.Text(["/start","start","شروع"]) ,self.start),
                CallbackQueryHandler(self.start,"start"),
                CallbackQueryHandler(self.update_server,"update_server"),
                CallbackQueryHandler(self.nonupdate_key,"nonupdate_key"),

                ConversationHandler(
                    entry_points=[CallbackQueryHandler(self.check_key,"check")],
                    states={
                        "check":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.check_key),CallbackQueryHandler(self.check_key)],
                        "details":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.check_key_detail),CallbackQueryHandler(self.check_key_detail)],
                        # "change":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,action),CallbackQueryHandler(action)]
                    },
                    fallbacks=[MessageHandler(filters.Text("/cancel"), self.cancel),CallbackQueryHandler(self.cancel,"cancel")],
                    ),

                ConversationHandler(
                entry_points= [CallbackQueryHandler(self.update_key,"update_key")],
                states={
                    "update_key" : [MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.update_key),CallbackQueryHandler(self.update_key)],
                    "get key": [MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.get_value),CallbackQueryHandler(self.get_value)],
                    "action":[MessageHandler(filters.TEXT &( ~ filters.COMMAND) ,self.action),CallbackQueryHandler(self.action)]
                },
                fallbacks=[MessageHandler(filters.Text("/cancel"), self.cancel),CallbackQueryHandler(self.cancel,"cancel")],
                ),


            ])
            app.add_error_handler(self.error)
            print('polling...')
            async with  app:
                await app.initialize()
                await app.start()
                await app.updater.start_polling()
                try:
                    await asyncio.Event().wait()
                    await app.stop
                except:
                    await app.stop
        except Exception as e:
            print(e)




