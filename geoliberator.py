# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Module Name: GeoLiberator
Functionality Purpose: Intake address data and apply data quality uniformity
6/13/19
'''

import pandas as pd
import re
import time
t0 = time.process_time_ns()

#Account for '&' and Saint(ST) and Fort(FT)
#Create full address parser
#Optimize code

class AddressError(BaseException):
    pass

class GeoLiberator:
    '''
    A class for instantiating governance & uniformity on full addresses
    GeoLiberator class takes in entire address as first argument and returns the instantiated GeoLiberator Object.
    One may manipulate object using member functions in order to parse certain properties of the address.
    Second 'log' argument set to return value by default or write to new specified file name.
    Third 'mode' argument set to False by default or True to print output results.

    Sample Code:

        from geoliberator import *
        GL_Object = GeoLiberator("123 Sample Street, New York 12345")
        GL_Object.getAddress(log="output_log.txt", mode=True) #This code should both print and create a log file
    '''

    def __init__(self, addr):
        self.addr = str(addr)
        self.streetTypesAll = ["STREET","STRE","STR","ST",
                   "AVENUE","AVEN","AVE","AV","AE",
                   "ROAD","RD","DRIVE","DR",
                   "PLACE","PLAC","PLCE","PL","PLC",
                   "BOULEVARD","BLVD","BOUL","BO",
                   "LANE","LN","COURT","CRT","CT",
                   "HEIGHTS","HTS","PARKWAY","PKWY",
                   "HIGHWAY","HWAY","HWY",
                   "EXPRESSWAY","EXPWA","EXPWY","EXPY","EXP",
                   "BROADWAY","BDWY","BWY","TURNPIKE","TPKE"]
        self.streetTypes = {"STREET": ["STREET","STRE","STR","ST"],
                            "AVENUE": ["AVENUE","AVEN","AVE","AV","AE"],
                            "ROAD": ["ROAD","RD"],
                            "DRIVE": ["DRIVE","DR"],
                            "PLACE": ["PLACE","PLAC","PLCE","PL","PLC"],
                            "BOULEVARD": ["BOULEVARD","BLVD","BOUL","BO"],
                            "LANE": ["LANE","LN"],
                            "COURT": ["COURT","CRT","CT"],
                            "HEIGHTS": ["HEIGHTS","HTS"],
                            "PARKWAY": ["PARKWAY","PKWY"],
                            "HIGHWAY": ["HIGHWAY","HWAY","HWY"],
                            "EXPRESSWAY": ["EXPRESSWAY","EXPWA","EXPWY","EXPY","EXP"],
                            "BROADWAY": ["BROADWAY","BDWY","BWY"],
                            "TURNPIKE": ["TURNPIKE","TPKE"]}

    def getCompass(self, direc):
        if 'N' == direc:
            return "NORTH"
        elif 'S' == direc:
            return "SOUTH"
        elif 'E' == direc:
            return "EAST"
        elif 'W' == direc:
            return "WEST"
        else:
            return False

    def getAddressNum(self, log='', mode=False):
        get = (self.addr).upper(); new_addr_num = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for sType in self.streetTypesAll:
            gANpat1 = re.search(fr"(?!\d+ ?{sType}(\W|$)\.?)(^\d+(-\d+)?)", get)
            if gANpat1 == None:
                new_addr_num = "OTHER"
                break
            elif gANpat1:
                new_addr_num = gANpat1.group()
        if log == '' and mode == True:
            print(new_addr_num)
        elif log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_address_numbers"
            if mode == True: #Print to standard output as well
                print(new_addr_num)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr_num + '\n')
            nf.close()
        return new_addr_num

    def getStreet(self, log='', mode=False):
        get = (self.addr).upper(); new_street = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for key in self.streetTypes:
            if new_street != '':
                break
            for sType in self.streetTypes[key]:
                gSpat1 = re.search(fr"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )({sType}\.?)(\W|$)", get)
                gSpat2 = re.search(fr"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)({sType}\.?)((?=\W)|$)", get)
                gSpat3 = re.search(fr"(?!\d)(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z])[ ,-]", get)
                if gSpat1:
                    if gSpat1.group(3) in self.streetTypes[key]:
                        new_street = self.getCompass(gSpat1.group(1)) + ' ' + gSpat1.group(2).strip(' ') + f" {key}"
                        break
                elif gSpat2:
                    if gSpat2.group(4) in self.streetTypes[key]:
                        new_street = gSpat2.group(1).strip(' ') + f" {key}"
                        break
                elif gSpat3:
                    new_street = "AVENUE " + gSpat3.group(2)
                    break
        if new_street == '':
            new_street = "OTHER"
        if log == '' and mode == True:
            print(new_street)
        elif log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_addresses"
            if mode == True: #Print to standard output as well
                print(new_street)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_street + '\n')
            nf.close()
        return new_street

    def getAddress(self, log='', mode=False):
        get = (self.addr).upper(); new_addr = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        gS = GeoLiberator(get).getStreet()
        gAN = GeoLiberator(get).getAddressNum()

        if log == '' and mode == True:
            print(new_addr)
        elif log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_addresses"
            if mode == True: #Print to standard output as well
                print(new_addr)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr + '\n')
            nf.close()
        return new_addr

t1 = time.process_time_ns()
total = t1 - t0
if __name__ == "__main__":
    print(f"Timestamp 1: {t0} n/s\nTimestamp 2: {t1} n/s")
    print("Module Time Elapsed:", total, "nanoseconds")
