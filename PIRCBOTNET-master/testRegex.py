import re

message = ":rajonali!rajonali@127.0.0.1 PRIVMSG #test :do i got it like that"
pattern = r':(.*)!(.*)@(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) PRIVMSG #(.*) :(.*)'
matches = re.match(pattern, message, re.M|re.I)
print matches.group(5)


