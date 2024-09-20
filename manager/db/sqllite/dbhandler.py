import sqlite3
class DbHandler:
    
    
    def __init__(self, dbpath):
        self.path = dbpath
        self.add_table_query = '''CREATE TABLE IF NOT EXISTS {} ( id INTEGER PRIMARY KEY )'''
        self.add_column_query = '''ALTER TABLE {} ADD COLUMN {} {}'''
        self.add_record_query = '''INSERT INTO {} ({}) VALUES ({})'''
        self.update_record_query = '''UPDATE {} SET {} WHERE {}'''
        self.delete_record_query = '''DELETE FROM {} WHERE {}'''
        self.list_table_query = '''SELECT name FROM sqlite_master WHERE type="table"'''
        self.list_column_query = '''PRAGMA table_info({})'''
        self.list_all_record_query = '''SELECT * FROM {}'''
        self.get_record_query = '''SELECT * FROM {} WHERE {} '''
        self.CONN = sqlite3.connect(self.path)
    
    
    
#####################################################
####                                             ####
####                  MAIN FUNCTIONS             ####
####                                             ####
#####################################################    
    
    def action(self,query,params: tuple=()):
        try: 
            self.CONN = sqlite3.connect(self.path)
            DB = self.CONN.cursor()
            DB.execute(query,params)
            self.CONN.commit()
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            self.CONN.close()





    def select(self,query):
        try:
            self.CONN =  sqlite3.connect(self.path)
            DB = self.CONN.cursor()
            resualt = DB.execute(query)
        except sqlite3.Error as e:
            print("Error:", e)
            resualt = e
        finally:
            return resualt
            


#####################################################
####                                             ####
####                  ADD SECTION                ####
####                                             ####
#####################################################


    def add_table(self,name):
        try:
            query = self.list_table_query + f"AND name='{name}'"
            row = self.select(query).fetchone()
            if row:
                return
                print(f"{name} table is already exist")
            else:
                query = self.add_table_query.format(name)
                self.action(query)
        except Exception as e:
            print(e)
        finally:
            self.CONN.close()
        

    



    def add_column(self,table,name,data_type):
        try:
            query = self.list_column_query.format(table)
            columns = self.select(query).fetchall()
            exist = False
            for col in columns:
                if col[1] == name:
                    exist = True
                    break
            if exist:
                return 0
                print(f"{name} colum is already exist in {table} table")
            else:
                query = self.add_column_query.format(table,name,data_type)
                self.action(query)
        except Exception as e:
            print(e)
        finally:
            self.CONN.close()







    def add_record(self,table,data: list={},condition: list={}):
        try:
            query = self.list_column_query.format(table)
            columns = self.select(query).fetchall()
            cols = []
            lis = []
            for col in columns:
                cols += [col[1]]
            # print(cols)
            query = ""
            for col in cols:
                if condition.get(col) != None:
                    lis += [f'{col} = "{condition.get(col)}"']
            # print(lis)
            # print(data)
            query = f"SELECT * FROM {table}  WHERE {' AND '.join(lis)}"
            # print(query)
            rows = self.select(query).fetchall()
            # print(rows)
            if rows:
                return 0
                # print("data is already exist")
            else:
                columns = ""
                values = ""
                for column , value in data.items():
                    columns += f"{column}"+","
                    values += f"\"{str(value)}\""+","
                values = values.removesuffix(",")
                columns = columns.removesuffix(",")
                query = self.add_record_query.format(table,columns,values)
                self.action(query)
            
        except Exception as e:
            print (e)
        finally:
            self.CONN.close()




#####################################################
####                                             ####
####                  SELECT SECTION             ####
####                                             ####
#####################################################

    def get_record(self,table,condition):
        try:
            condi = []
            for (column , value) in condition.items():
                condi += [ f"{column} LIKE \'%{str(value)}%\' "]
            query = self.get_record_query.format(table,' AND '.join(condi))
            print(query)
            # print(self.select(query).fetchall())
            return self.select(query).fetchall()
        except Exception as e:
            print(e)


    def list_tables(self):
        query = self.list_table_query
        tables = self.select(query).fetchall()
        table_names = [table[0] for table in tables]
        for name in table_names:
            print(name)





    def list_columns(self,table):
        query = self.list_column_query.format(table)
        columns = self.select(query).fetchall()
        column_number = [column[0] for column in columns]
        column_names = [column[1] for column in columns]
        column_type = [column[2] for column in columns]
        # print(column_names)
        column_info = []
        column_allinfo = []
        for number,name,type in zip(column_number, column_names, column_type):
            column_allinfo += ["{} {} {}".format(number,name,type)]
            column_info += ["{}".format(name)]
            
            # print("{} {} {}".format(number,name,type))
        return column_info
    



    def list_all_record(self,table):
        self.CONN = sqlite3.connect(self.path)
        query = self.list_all_record_query.format(table)
        records = self.select(query)
        rows = records.fetchall()
        self.CONN.close()
        return rows




    def update(self, table, condition: str ={} ,data: str = {}):
        try:
            query = self.list_column_query.format(table)
            columns = self.select(query).fetchall()
            cols = []
            lis = []
            for col in columns:
                cols += [col[1]]
            query = ""
            for col in cols:
                if condition.get(col) != None:
                    lis += [f'{col} = "{condition.get(col)}"']
            # print(lis)
            query = f"SELECT * FROM {table}  WHERE {' AND '.join(lis)}"
            rows = self.select(query).fetchall()
            if rows:
                # print(rows)
                condi = []
                datalist=[]
                for (column , value) in condition.items():
                    condi += [ f'{column} = "{value}"']

                for (datac , dataval) in data.items():
                    datalist += [f"{datac}=\"{dataval}\""]
                query = self.update_record_query.format(table,f' , '.join(datalist),f' AND '.join(condi))
                # print(query)
                self.action(query)  
                # self.get_record(table=table,condition=condition)
                # print("################################################################################")
            else:
                print("not found record")
        except Exception as e:
            print (e)
        finally:
            self.CONN.close()


    def delete_record(self, table , condition):
        query = self.delete_record_query.format(table,condition)
        self.action(query)

