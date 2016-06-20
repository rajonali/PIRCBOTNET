import json
import os
import socket
import sqlite3
import sys
import string


class irc():
    config = "helper/config.json"
    banner = "helper/banner.motd"

    def __init__(self):
        try:
            with open(self.config, 'r') as f:
                self.config = json.loads(f.read())
        except Exception as e:
            print(e)
        try:
            self.irc_host = self.config["host"]
            self.irc_port = self.config["port"]
            self.irc_channel = self.config["channel"]
            self.irc_nick = self.config["master-nick"]
        except Exception as e:
            print(e, "Check out host, port, channel, and master-nick entries in helper/config.py")

    def set_motd(self):
        self.version = self.config["version"]
        self.authors = self.config["author"]
        self.motd = self.config["motd-location"]
        banner_buffer = []
        banner = open(self.banner)
        try:
            motd = open(self.motd, 'w')
        except Exception as e:
            print(e ,"Try running with super user perms.")
        for line in banner:
            banner_buffer.append(line)
        motd.write(str("".join(banner_buffer))  + " Version:: %s " %str(self.version)  + "\n" + " Author(s):: %s" %str(", ".join(self.authors)) +  "\n" + (" "+"="*42) + "\n")

    def connect_server(self):
	client_socket = socket.socket()
	client_socket.connect((self.irc_host, self.irc_port))
	#client_socket.send("NICK %s\r\n" % (self.irc_nick))
	#client_socket.send("USER rajonali rajonpi.noip.me rajonali :Rajon Ali\r\n")
	#client_socket.send("JOIN %s\r\n" % (self.irc_channel))
    def listen_server(self, sock):
	sock.recv(1024))
    def set_username(self, sock, params):
	sock.send("USER %s\r\n" %(*params))
    def set_nickname(self, sock, nickname):
	sock.send("NICK %s\r\n" % (nickname))
    def join_channel(self, sock, channel):
	sock.send("JOIN %s\r\n" % (channel))
    def send_command(self, sock, command):
        sock.send("%s\r\n" % (command))
    def give_perms(self, sock):
        pass
    def message(self, sock, message, user):
	sock.send("PRIVMSG %s :" %(user) + message +"\r\n")
    def message_channel(self, sock, message, channel):
	self.message(sock, message, channel)
    def quit(self, sock):
	self.send_command(sock, "/QUIT")
	sock.close()
    def pongmyping(self, sock):
	if "PING" in sock.recv(1024):
	    sock.send("PONG\r\n")
	

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
            self.connect_db(self,db,*args, **kwargs)
    
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

    def	insert_db(self, fields, data):
	return self.execute('INSERT INTO %s %s VALUES %s' % (str(self.db), str(fields), str(data)))
	self.commit()

    def create_table(self, typesndata)
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
        con.commit()i

class plugin():
    pass

def main():
    inst1 = irc()
    #inst1.set_motd()


if __name__ == '__main__':
    main()
