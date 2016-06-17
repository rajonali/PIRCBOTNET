import json
import os


class irc():
    config = "helper/config.json"
    banner = "helper/banner.motd"
    motd = None
    version = None
    authors = None

    def __init__(self):
        with open(self.config, 'r') as f:
            self.config = json.load(f)
        self.set_motd()

    def set_motd(self):
        self.versions = self.config["version"]
        self.authors = self.config["author"]
        self.motd = self.config["motd-location"]
        banner_buffer = []
        banner = open(self.banner)
        motd = open(self.motd, 'w')
        for line in banner:
            banner_buffer.append(line)
        motd.write("".join(banner_buffer))
        with open(self.motd, 'a'):
            self.motd.append(" version: %s /n author(s): %s /n" % str(self.version), str(", ".join(self.authors)))


class conn_db():
    pass

class plugin():
    pass


def main():
    inst1 = irc()
    inst1.set_motd()



if __name__ == '__main__':
    main()
