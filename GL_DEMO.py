# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: GeoLiberator Demo
Functionality Purpose: Demonstrate the address parsing module 'GeoLiberator'
7/2/19
'''
#Single Address Test
#Upload file for multiple addresse
#Print liberated output

from geoliberator import *

address = input("Enter any address: ")
print("0 - Street Name\n1 - AHouse Number\n2 - Full Address")
m = int(input("Enter a number 0-2: "))
if address == '':
    address = "123 Main St, (Default Test Address)"
print("Before: ", address, "\nAfter: ", end='')
geoLiberate(address, m)

input("Press Enter to Exit...")
exit()
