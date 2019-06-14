# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Module Name: GeoLiberator
Functionality Purpose: Intake address data and apply data quality uniformity
6/14/19
'''
#Alpha 1.0

import re
import time
t0 = time.process_time_ns()

#Account for '&' and Saint(ST) and Fort(FT)
#Acount for all street types
#Option to append borough, state, zip, based on argument

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
                   "ROAD","RD","RO","DRIVE","DR",
                   "PLACE","PLAC","PLCE","PL","PLC",
                   "BOULEVARD","BLVD","BOUL","BO",
                   "LANE","LN","COURT","CRT","CT",
                   "HEIGHTS","HTS","PARKWAY","PKWY",
                   "HIGHWAY","HWAY","HWY",
                   "EXPRESSWAY","EXPWA","EXPWY","EXPY","EXP",
                   "BROADWAY","BDWY","BWY","TURNPIKE","TPKE"]
        self.streetTypes = {"STREET": ["STREET","STRE","STR","ST"],
                            "AVENUE": ["AVENUE","AVEN","AVE","AV","AE"],
                            "ROAD": ["ROAD","RD","RO"],
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
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for sType in self.streetTypesAll:
            gANpat1 = re.search(fr"(?!\d+ ?{sType}(\W|$)\.?)(^\d+(-\d+)?)", get)
            if gANpat1 == None:
                new_addr_num = "OTHER"
                break
            elif gANpat1:
                new_addr_num = gANpat1.group()
        if log == '' and mode == True: #Print to standard output and return value
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
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for key, val in self.streetTypes.items():
            if new_street != '':
                break
            sType = '|'.join(val)
            getStreetPattern1 = re.search(fr"(?!\d)([NSEW])(\.? ?\d+ ?| [A-Z]+ )({sType})\.?(\W|$)", get)
            getStreetPattern2 = re.search(fr"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)({sType})\.?((?=\W)|$)", get)
            getStreetPattern3 = re.search(fr"(?!\d)?(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z])[ ,-]", get)
            if getStreetPattern1:
                if getStreetPattern1.group(3) in self.streetTypes[key]:
                    new_street = self.getCompass(getStreetPattern1.group(1)) + ' ' + getStreetPattern1.group(2).strip(' ') + f" {key}"
                    break
            elif getStreetPattern2:
                if getStreetPattern2.group(4) in self.streetTypes[key]:
                    new_street = getStreetPattern2.group(1).strip(' ') + f" {key}"
                    break
            elif getStreetPattern3:
                new_street = "AVENUE " + getStreetPattern3.group(2)
                break
        if new_street == '':
            new_street = "OTHER"
        if log == '' and mode == True: #Print to standard output and return value
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
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        gS = GeoLiberator(get).getStreet()
        gAN = GeoLiberator(get).getAddressNum()
        if gAN != "OTHER" and gS != "OTHER":
            new_addr = gAN + ' ' + gS
        else:
            new_addr = "OTHER"
        if log == '' and mode == True: #Print to standard output and return value
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
