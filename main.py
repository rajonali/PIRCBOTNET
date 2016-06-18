import json
import os
import socket


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
        motd = open(self.motd, 'w')
        for line in banner:
            banner_buffer.append(line)
        motd.write(str("".join(banner_buffer))  + " Version:: %s " %str(self.version)  + "\n" + " Author(s):: %s" %str(", ".join(self.authors)) +  "\n" + (" "+"="*42) + "\n")

    def connect_server(self):
	pass
    def join_channel(self):
	pass
    def send_command(self):
	pass
    def 



class conn_db():
    pass

class plugin():
    pass


def main():
    inst1 = irc()
    inst1.set_motd()



if __name__ == '__main__':
    main()
