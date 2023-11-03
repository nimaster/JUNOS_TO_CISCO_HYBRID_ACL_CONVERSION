import os

x = 1
while x < 200:
    os.system("rm term%s"%x)
    x+=1
