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

def padNum(num):
    num = str(num)[0:5]
    return num

def file_len(file_name):
    with open(file_name) as f:
        for i, L in enumerate(f):
            pass
    return i + 1

file = "new.txt"
if sys.argv[1] == '--status' or sys.argv[1] == "-S":
    f = open(file); lines = f.readlines(); FL = file_len(file)
    barIncr = int(FL * .025); barNum = 0; dashNum = 40; c = 0; lc = 0
    for line in lines:
        perc = (lc/FL) * 100
        bar = '|' + ('█' * barNum) + ('-' * dashNum) + '|' + " [{:>}]".format(padNum(perc))
        c += 1; lc += 1
        if c == barIncr:
            if barNum < 39:
                c = 0; barNum += 1; dashNum -= 1
                print(f"\r{bar}", end=''); sys.stdout.flush()
                time.sleep(.025)
    print('\r|' + ('█' * 40) + '|' + " [100%]"); sys.stdout.flush()
                
