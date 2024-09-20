from .dbhandler import DbHandler 
class VpnDb:
    def __init__(self, database) -> None:
        self.db = DbHandler(database)
        self.tables = {
            "users" : {
                        "user_id" : "TEXT",
                        "teleid":"TEXT",
                        "baleid":"TEXT",
                        "phone":"TEXT",
                        "email":"TEXT",
                    },
            "keys" : {
                        "access_url":"TEXT",
                        "data_limit":"TEXT",
                        "key_id":"TEXT",
                        "method":"TEXT",
                        "name":"TEXT",
                        "password":"TEXT",
                        "port":"TEXT",
                        "used_bytes":"TEXT",
                        "expire_date":"TEXT",
                        "status":"TEXT",
                    },
            "ownership":{
                        "key_id":"TEXT",
                        "manager":"TEXT",
                        "consumer":"TEXT",
                    },
            "payment":{
                        "user_id":"TEXT",
                        "date":"TEXT",
                        "amount":"TEXT",
                        "methode":"TEXT",
                        "request":"TEXT",
                    },
        }
        # self.all = self.db.list_all_record("keys")



    def info(self,mode,table,value):
        self.all = self.db.list_all_record(table)
        self.query = self.db.list_column_query.format(table)
        self.attrs = [column[1] for column in self.db.select(self.query).fetchall()]
        key = {}
        try: 
            for attr in self.attrs:
                setattr(self, attr, self.get_object(mode,value)[self.attrs.index(attr)] )
                key[attr] = self.get_object(mode,value)[self.attrs.index(attr)]
            return key
        except Exception as e:
            print("FOR ERROR :",e)



    def update(self,table,key):
        # print(key)
        self.db.update(table=table,condition={"key_id":f'{key["key_id"]}'},data=key)

        
    def get_object(self,attr,value):
        try:
            for user in self.all: 
                ins = user[self.attrs.index(attr)]
                if ins == value:
                    return [user[self.attrs.index(col)] for col in self.attrs]
        except Exception as e :
            print(e)




    def make_db(self):
        for table in self.tables.keys():
            self.db.add_table(table)
            for column,type in self.tables[table].items():
                self.db.add_column(table=table,name=column,data_type=type)