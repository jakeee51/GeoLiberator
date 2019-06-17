# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Module Name: GeoLiberator
Functionality Purpose: Intake address data and apply data quality uniformity(intantiate data governance)
6/17/19
'''
#Alpha 1.0

import re
import time
t0 = time.process_time_ns()

#Account for '&' and 'STS'
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
        self.streetTypes = {"STREET": ["STREET","STRE","STR","ST"],
                            "AVENUE": ["AVENUE","AVEN","AVE","AV","AE"],
                            "ROAD": ["ROAD","RD","RO"],
                            "DRIVE": ["DRIVE","DRIV","DR"],
                            "PLACE": ["PLACE","PLAC","PLCE","PL","PLC"],
                            "BOULEVARD": ["BOULEVARD","BLVD","BOUL","BLV","BO"],
                            "COURT": ["COURT","CRT","CT"],
                            "HEIGHTS": ["HEIGHTS","HTS"],
                            "PARKWAY": ["PARKWAY","PKWAY","PKWY","PWY","PKY"],
                            "HIGHWAY": ["HIGHWAY","HWAY","HWY"],
                            "BROADWAY": ["BROADWAY","BDWY","BWY"],
                            "EXPRESSWAY": ["EXPRESSWAY","EXPRESWY","EXPRESWAY","EXPREWAY","EXPWA","EXPWY","EXPY","EXWY","EXP"],
                            "PLAZA": ["PLAZA","PLAZ","PLZA","PLZ"],
                            "CONCOURSE": ["CONCOURSE","CONC","CNCRS","CON","CO"],
                            "TERRACE": ["TERRACE","TERR","TER","TE"],
                            "CRESCENT": ["CRESCENT","CRESCNT","CRES"],
                            "ALLEY": ["ALLEY","ALY"],
                            "GARDENS": ["GARDENS","GDNS"],
                            "ESPLANADE": ["ESPLANADE","ESPL"],
                            "PARK": ["PARK","PRK","PK"],
                            "HILL": ["HILL","HL"],
                            "LANE": ["LANE","LN"],
                            "PROMENADE": ["PROMENADE","PROM"],
                            "COURSE": ["COURSE","CRSE"],
                            "FREEWAY": ["FREEWAY","FWY"],
                            "TURNPIKE": ["TURNPIKE","TPKE"],
                            "SQUARE": ["SQUARE","SQ"],
                            "CIRCLE": ["CIRCLE","CIR"],
                            "CLOSE": ["CLOSE","CLOS"],
                            "VILLAGE": ["VILLAGE","VLG"],
                            "RIDGE": ["RIDGE","RDG"],
                            "COVE": ["COVE","CV"],
                            "TRAIL": ["TRAIL","TRL"],
                            "GREEN": ["GREEN","GRN"],
                            "CAMP": ["CAMP","CP"],
                            "SLIP": ["SLIP"],"LOOP": ["LOOP"], "WAY": ["WAY"],"EST": ["EST"],"ROW": ["ROW"],"OVAL": ["OVAL"],"PATH": ["PATH"]}
        hold = ''
        for typ in self.streetTypes:
            hold += re.sub(r"[\[\]' ]", '', str(self.streetTypes[typ])) + ','
        self.streetTypesAll = list(hold.strip(',').split(','))

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
            getStreetPattern1 = re.search(fr"(?!\d)?([NSEW])(\.? ?\d+ ?| [A-Z]+ )({sType})\.?(\W|$)", get)
            getStreetPattern2 = re.search(fr"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z]+ )+)({sType})\.?((?=\W)|$)", get)
            getStreetPattern3 = re.search(fr"(?!\d)?(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF THE [A-Z]+)([ ,-]|$)", get)
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
        new_street = re.sub(r"^FT\W| FT\W", "FORT ", new_street)
        new_street = re.sub(r"^ST\W| ST\W", "SAINT ", new_street)
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
