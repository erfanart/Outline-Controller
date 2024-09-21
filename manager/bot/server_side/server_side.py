
from telegram import Update
from telegram.ext import ConversationHandler,BaseHandler,JobQueue , filters, ContextTypes
import asyncio , time
from manager import vpn
from manager.bot.client_side import *
from manager.vpn.server import Server
from manager.setting import *
from manager.vpn import *




class Server_Side(Cient_Side):
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


    async def check_key_detail(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        method = context.user_data["check_method"]
        text = context.user_data["check_method_text"]
        selected_keys = self.keys.vpndb.db.get_record(table="keys",condition={str(method):str(text)})
        try:
            query = update.callback_query.data  
            print("check_key_detail function:",query)
            checking = any(query in k[6] for k in selected_keys)
            if checking:
                for k in selected_keys:
                    if query in k[6]:
                        usage = round(float(k[8])/pow(10,9),3)
                        limit = round(float(k[2])/pow(10,9),3) 
                        text= f"""
نام کلید: {k[5]}
پورت کلید: {k[7]}
تاریخ انقضا: {k[9]}
حجم باقی مانده: {limit - usage}G
"""                 
                        btn={
                            "limit":"تغییر حجم",
                            "date":"تغییر تاریخ انقضا",
                            "back":"بازگشت"

                        }
                        context.user_data["key_pass"] = k[6]
                        btn= await self.make_inline_key(BUTTONS=btn)
                        await self.send_message(update=update,context=context,text=text,key=btn)
            if query == "back":
                btn={}
                for k in selected_keys: 
                    btn[str(k[6])] = str(k[5])
                btn["rechoose"] = "بازگشت"
                btn= await self.make_inline_key(BUTTONS=btn)
                await self.send_message(update=update,context=context,text=" کلید های یافت شده به صورت زیر میباشد:",key=btn)
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
            elif query == "rechoose":
                context.user_data["check_method"]=None
                await self.check_key(update=update,context=context)
                return "check"        
        except Exception as e:
           try:
            key_pass = context.user_data["key_pass"]
            method = context.user_data["method"] 
            if method == "date":             
                try:
                    k = self.keys.vpndb.info("password","keys",key_pass)
                    print(k)
                    text = int(update.message.text)
                    self.keys.vpndb.update(key=k,method="date",unit=text)
                    context.user_data["key_pass"] = ""
                    context.user_data["method"]  = ""
                    vpn.update()
                    btn = await self.make_inline_key({"back":"بازگشت"})
                    await self.send_message(update=update,context=context,text="عملیات با موفقیت انجام شد",key=btn)
                except Exception as e:
                    print("action function Thired exseption: ", e)
                    await self.send_message(update=update,context=context,text=f"خطا در {e}")
                    await self.start(update=update,context=context)
                    return ConversationHandler.END
            elif method == "limit":
                try:
                    k = self.keys.vpndb.info("password","keys",key_pass)
                    text = int(update.message.text)
                    context.user_data["key_pass"] = ""
                    context.user_data["method"]  = ""
                    self.keys.vpndb.update(key=k,method="limit",unit=text)
                    vpn.update()
                    btn = await self.make_inline_key({"back":"بازگشت"})
                    await self.send_message(update=update,context=context,text="عملیات با موفقیت انجام شد",key=btn)
                except Exception as e:
                    print("action function Thired exseption: ", e)
                    await self.send_message(update=update,context=context,text=f"خطا در {e}")
                    await self.start(update=update,context=context)
                    return ConversationHandler.END
            elif method == "":
                btn={}
                for k in selected_keys: 
                    btn[str(k[6])] = str(k[5])
                    print(k[5])
                btn["rechoose"] = "بازگشت"
                print(btn)
                btn= await self.make_inline_key(BUTTONS=btn)
                await self.send_message(update=update,context=context,text=" کلید های یافت شده به صورت زیر میباشد:",key=btn)

           except Exception as e:
                print("check_key_detail error : ",e)
                btn={}
                for k in selected_keys: 
                    btn[str(k[6])] = str(k[5])
                    print(k[5])
                btn["rechoose"] = "بازگشت"
                print(btn)
                btn= await self.make_inline_key(BUTTONS=btn)
                await self.send_message(update=update,context=context,text=" کلید های یافت شده به صورت زیر میباشد:",key=btn)
    

    async def check_key(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
            try:
                query = update.callback_query.data  
                print(query)
                if query == "name":
                    btn ={
                        "back":"بازگشت"
                        }
                    btn = await self.make_inline_key(btn)
                    context.user_data["check_method"] = "name"
                    await self.send_message(update=update,context=context,text=" نام کلید مد نظر را وارد کنید",key=btn)
                elif query == "port":
                    btn ={
                        "back":"بازگشت"
                        }
                    btn = await self.make_inline_key(btn)
                    context.user_data["check_method"] = "port"
                    await self.send_message(update=update,context=context,text=" پورت کلید مد نظر را وارد کنید",key=btn)
                elif query == "key_id":
                    btn ={
                        "back":"بازگشت"
                        }
                    btn = await self.make_inline_key(btn)
                    context.user_data["check_method"] = "key_id"
                    await self.send_message(update=update,context=context,text=" شناسه کلید مد نظر را وارد کنید",key=btn)
                elif query == "return":
                    await self.start(update=update,context=context)
                    return ConversationHandler.END
                else:
                    btn ={
                        "name":"براساس نام",
                        "port":"براساس پورت اختصاص داده شده",
                        "key_id":"بر اساس شناسه ی کلید",
                        "return":"بازگشت"
                    }
                    context.user_data["check_method"]=None
                    btn= await self.make_inline_key(BUTTONS=btn)
                    await self.send_message(update=update,context=context,text=" مشخصات کلید خود را وارد کنید",key=btn)
                    return "check"
                
            except Exception as e:
                method = context.user_data["check_method"]
                text = update.message.text
                if method is not None:
                    if method == "name" or method == "port" or method == "key_id":
                        context.user_data["check_method_text"]=text
                        await self.check_key_detail(update=update,context=context)
                        return "details"
                    else:
                        await self.send_message(update=update,context=context,text="این مدل جستجو موجود نیست")  
                        btn ={
                            "name":"براساس نام",
                            "port":"براساس پورت اختصاص داده شده",
                            "key_id":"بر اساس شناسه ی کلید",
                            "return":"بازگشت"
                        }
                        btn= await self.make_inline_key(BUTTONS=btn)
                        await self.send_message(update=update,context=context,text=" مشخصات کلید خود را وارد کنید",key=btn)
                        return "check"    
                else:
                    await self.send_message(update=update,context=context,text="ابتدا مدل جستجوی کلید مدنظر را انتخاب کنید")  
                    btn ={
                        "name":"براساس نام",
                        "port":"براساس پورت اختصاص داده شده",
                        "key_id":"بر اساس شناسه ی کلید",
                        "return":"بازگشت"
                    }
                    btn= await self.make_inline_key(BUTTONS=btn)
                    await self.send_message(update=update,context=context,text=" مشخصات کلید خود را وارد کنید",key=btn)
                    return "check"


    async def expired_key(self):
        print("welcome to expire if")
        keys = self.keys.vpndb.db.get_record(table="keys",condition={"status":"limited"})
        txt ="--------------------------------------------------------"+"\n"
        txt += "LIMITED KEYS:"
        for k in keys:
            ke = self.keys.vpndb.info(mode="key_id",table="keys",value=k[3])
            try:
                usage = str(float(ke["used_bytes"])/pow(10,9))
            except:
                usage="None"

            txt +=  "\n"+"<< " + f'key:{ke["name"]} key_id:{ke["key_id"]} status:{ke["status"]} usage:{usage}'+" >>"
        txt +=  "\n"+"--------------------------------------------------------"
        keys = self.keys.vpndb.db.get_record(table="keys",condition={"status":"expired"})
        txt += "\n"+"EXPIRED KEYS:"
        for k in keys:
            ke = self.keys.vpndb.info(mode="key_id",table="keys",value=k[3])
            txt +=  "\n"+"<< " + f'key:{ke["name"]} key_id:{ke["key_id"]} status:{ke["status"]} date:{ke["expire_date"]}'+" >>"
        txt +=  "\n"+"--------------------------------------------------------"
        return txt


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


