import json
import os
import socket
import sqlite3


class irc():
    config = "helper/config.json"
    banner = "helper/banner.motd"
    motd = None
    version = None
    authors = None
    irc_host = None
    irc_port = None
    irc_cmdchannel = None
    irc_botchannel = None
    users_db = None    

    def __init__(self):
        try:
            with open(self.config, 'r') as f:
                self.config = json.loads(f.read())
        except Exception as e:
            print(e)

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
        pass
    def join_channel(self):
        pass
    def send_command(self):
        pass
    def give_perms(self):
	pass


class conn_db():
    cursor = None
    def __init__(self, db, *args, **kwargs):
	self.database = db
        print("Connecting to database...")
	try:
            self.conn = sqlite3.connect(str(self.database), *args, **kwargs)
            print("SUCCESSFULLY CONNECTED TO DATABASE.")
	    self.cursor = self.conn.cursor()
	    return self.cursor
	except Exception as e:
	    print("UNABLE TO CONNECT TO DATABASE. Trying again...")
	    sleep(1)
	    self.connect_db(self,db,*args, **kwargs)

    def execute(self, command):
        return self.users_db.execute(str(command))

    def commit(self):
        connec
    def close_db(self):
	return self.users_db.close()

 
class plugin():
    pass


def main():
    inst1 = irc()
    inst1.set_motd()



if __name__ == '__main__':
    main()
