import json
import os
import socket
import sqlite3
import sys
import string

class conn_db():
    def __init__(self, db, *args, **kwargs):
        self.db = db
        print("Connecting to database...")
        try:
            self.conn = sqlite3.connect(str(self.db), *args, **kwargs)
            print("SUCCESSFULLY CONNECTED TO DATABASE.")
            return self.conn
            #return self.cursor
        except Exception as e:
            print("UNABLE TO CONNECT TO DATABASE. Trying again...")
            sleep(2)
            #CHECK IF PARAMS MATCH
            self.__init__(self,db,*args, **kwargs)

    def gettime(self):
        return str(datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))

    def cursor(self):
        return self.conn.cursor

    def execute(self, command):
        return self.cursor().execute(str(command))

    def commit(self):
        return self.conn.commit()

    def close_db(self):
        return self.conn.close()

    def insert_db(self, fields, data):
        return self.execute('INSERT INTO %s %s VALUES %s' % (str(self.db), str(fields), str(data)))
        self.commit()

    def create_table(self, typesndata):
        return 'CREATE TABLE IF NOT EXISTS %s %s' % (str(self.db), str(typesndata))
        self.commit()

    def select_table(self, fields="*"):
        return 'SELECT %s FROM %s' % (str(self.db), str(fields).replace("(", "").replace(")", ""))
        self.commit()

    def getdbsize(self):
        size = self.execute('SELECT * FROM %s' % str(self.db))
        return len(size.fetchall())

    def deleteID(self, id_field, id):
        self.execute('DELETE FROM %s WHERE id= %s')
        con.commit()

