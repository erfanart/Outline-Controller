from manager.db import VpnDb
from manager.setting import *
import jdatetime




class Keys:
    def __init__(self,server) -> None:
        self.server = server
        self.all = server.get_keys()
        self.vpndb = VpnDb().AppDB


    def info(self,mode,value):
        self.keyratt = [] 
        for attr in dir(self.all[0]):
            if not callable(getattr(self.all[0], attr)) and not attr.startswith("__"):
                self.keyratt += [attr]
        type(self).attrs = self.keyratt
        key={}
        for attr in self.attrs:
            setattr(type(self), attr, self.get_key(mode,value)[self.attrs.index(attr)] )
            key[attr] = f"{self.get_key(mode,value)[self.attrs.index(attr)]}"
        return key





    def get_key(self,attr,value):
        for key in self.all :
            if getattr(key , attr) == value:
                return [getattr(key, att) for att in self.attrs]
            


    def check_usage(self,key):
        if key["used_bytes"] == 'None' :
            usage = 0
        else:
            usage = round(float(key["used_bytes"])/pow(10,9),3)
        if key["data_limit"] == 'None':
            limit = 0
        else:
            limit = round(float(key["data_limit"])/pow(10,9),3) 
        if limit - usage < 1:
           # print(key["name"],"with keyid:" ,key["key_id"] ,"is limited")
            status="limited"
        else:
            status = "active"
        return status

            
    def check_date(self,key):
        now = jdatetime.datetime.now()
        try:
            expire = jdatetime.datetime.strptime(key["expire_date"],"%Y/%m/%d")
        except:   
            return "None"
        if jdatetime.timedelta(days= -10) < expire - now < jdatetime.timedelta(days=1):
            #print(key["name"],"with keyid:" ,key["key_id"] ,"is limited")
            self.set_limit(key,0)
            return "expired"
        else:
            return "active"
        

    def check_exist(self,key):
        # print("Check Exit Function")
        all = self.all
        for k in all:
            flag = False
            # print("check exition of:" , k.key_id)
            if key["key_id"] == k.key_id:
                flag = True
                break
        return flag
    

    def check_status(sef,key):
        print(key)
        return key
    


    def active_key(self,key,method,unit: int=1):
        if method == "date":
            key = self.extend_expire(key=key,unit=unit)
            # print("date",key)
            self.vpndb.update(table="keys",key=key)

        elif method == "limit":
            self.set_limit(key=key,unit=unit)
            print("method is limit")


    def set_limit(self,key,unit: int=1):
        unit = unit * pow(10,9)
        # print(unit)
        self.server.add_data_limit(key_id=key["key_id"],limit_bytes=unit)


    def extend_expire(self,key,unit: int=30):
        now = jdatetime.datetime.now()
        expire = now + jdatetime.timedelta(days=unit)  
        key["expire_date"] = expire.strftime("%Y/%m/%d")
        return key