# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: GeoLiberator Demo
Functionality Purpose: Demonstrate the address parsing module 'GeoLiberator'
Version: Beta
'''

#Single Address Test
#Upload file for multiple addresses
#Display liberated output

from GeoLiberator import *
import time
import sys

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

a = "Welcome to the GeoLiberator Application\n"
for i in a:
    print(i, end='')
    time.sleep(.02)
b = """This application demonstrates this Python module's ability
to intake messy addresses and output uniform addresses\n"""
for i in b:
    print(i, end='')
    time.sleep(.02)
print("Type 'quit' to exit...\n")
while True:
    address = input("Enter any address: ")
    if address.lower() == "exit" or address.lower() == "quit":
        exit()
    print("street - Street Name\n1 - House Number\n2 - Full Address")
    m = int(input("Enter a number 0-2: "))
    if address == '':
        address = "123 Main St, (Default Test Address)"
    print("Before: ", address, "\nAfter: ", end='')
    if m == 2:
        m = "address"
    elif m == 1:
        m = "number"
    elif m == 0:
        m = "street"
    geoLiberate(address, m)
