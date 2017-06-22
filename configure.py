'''
Use to setup motd files and create databases. Configure config file before running this script.
'''

import sys
import json
import os
import socket
import sqlite3
import string
from helper.IRC import irc

config = "helper/config.json"
banner = "helper/banner.motd"


def main():
    inst1 = irc(config,banner)
    inst1.set_motd()
    inst1.connect_server()
    botnick = "Gru"
    channel = "#test"
    inst1.set_username('master-Gru')
    inst1.set_nickname(botnick)
    inst1.join_channel(channel)
    for i in range(10):
        try:
	        inst1.message_channel("woowebangintoo", "#test")
    	except KeyboardInterrupt:
            print "Closing connection and exiting... "
            inst1.quit()
            sys.exit()

if __name__ == '__main__':
    main()
