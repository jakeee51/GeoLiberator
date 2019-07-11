# -*- coding: utf-8 -*-

import sys
import time

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def file_len(file_name):
    with open(file_name) as f:
        for i, L in enumerate(f):
            pass
    return i + 1

bar = 0; dash = 5
a = '█'*bar
b = '-'*dash
BAR = "|" + a + b + "|"
print(BAR, end=''); sys.stdout.flush()
for i in range(5):
    bar += 1; dash -= 1
    print('\r' + BAR, end=''); sys.stdout.flush()
    time.sleep(.25)

##file = "new.txt"
##if sys.argv[1] == '--status' or sys.argv[1] == "-S":
##    f = open(file); lines = f.readlines(); FL = file_len(file)
##    barIncr = int(FL * .025); barNum = 0; dashNum = 40; c = 0
##    bar = '|' + ('█' * barNum) + ('-' * dashNum) + '|'
##    print(bar, end=''); sys.stdout.flush()
##    for line in lines:
##        c += 1
##        if c == barIncr:
##            if barNum < 39:
##                c = 0; barNum += 1; dashNum -= 1
##                print(f"\r{bar}", end=''); sys.stdout.flush()
##                time.sleep(.025)
##    print('\r|' + ('█' * 40) + '|')
                
