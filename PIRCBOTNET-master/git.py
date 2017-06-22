import sys,os

os.system("git add *") 
def commit():
    os.system("git commit -m " + sys.argv[1]) 
ans = input("Are you sure? y/N")
if (ans == "y"):
    commit()
else: 
    print("Aborted")
os.system("git push")
