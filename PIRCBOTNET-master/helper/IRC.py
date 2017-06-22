import json
import os
import socket
import sqlite3
import sys
import string


class irc():

    def __init__(self, config, banner):
        self.config = config
        self.banner = banner
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
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.irc_host, self.irc_port))
        #client_socket.send("NICK %s\r\n" % (self.irc_nick))
        #client_socket.send("USER rajonali rajonpi.noip.me rajonali :Rajon Ali\r\n")
        #client_socket.send("JOIN %s\r\n" % (self.irc_channel))
    def listen_server(self):
        self.client_socket.recv(1024)
    def set_username(self, botnick):
        self.client_socket.send("USER " + botnick + " " + botnick +" " + botnick + " :I am alive!\r\n")
    def set_nickname(self, botnick):
        self.client_socket.send("NICK " + botnick + "\r\n")
    def join_channel(self, channel):
        self.client_socket.send("JOIN " + channel + "\r\n")
    def send_command(self, command):
        self.client_socket.send("%s\r\n" % (command))
    def give_perms(self):
        pass
    def message(self, message, username):
        self.client_socket.send("PRIVMSG %s :" %(username) + message +"\r\n")
    def message_channel(self, message, channel):
        self.client_socket.send("PRIVMSG " + channel + " " + message + "\r\n")
    def quit(self):
        self.client_socket.send_command("/QUIT")
        self.client_socket.close()
    def get_text(self):
        text=self.client_socket.recv(2040)  #receive the text
	print(text)
        if 'PING' in text:
            self.irc.send('PONG ' + text.split() [1] + '\r\n')
        return text

