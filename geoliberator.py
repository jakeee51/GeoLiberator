import pandas as pd
import re

#Account for no address number and cardinal direction beginning
#Account for for '&' and Saint(ST) and Fort(FT)
#Create full address parser
#Clear further to pick up mismatches

class AddressError(BaseException):
    pass

class GeoLiberator:
    '''
    A class for instantiating governance & uniformity on full addresses

    GeoLiberator class takes in entire address as first argument and returns the instantiated GeoLiberator Object.
    One may manipulate object using member functions in order to parse certain properties of the address.
    Second 'mode' argument set to 'print' by default to print to standard output or write to new specified file name.
    '''
    def __init__(self, addr):
        self.addr = str(addr)
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
    def getAddressNum(self, mode=0, log=False):
        get = (self.addr).upper(); new_addrNum = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        if re.search(r"^\d+(-\d+)?", get):
            grab = re.search(r"^\d+(-\d+)?", get) #___NOT followed by street type___
            #new_addrNum = ...
        if mode == 0:
            print(new_addrNum)
        else: #Write to new or specfied file
            fileName = re.sub(r"\..+", '', mode)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_address_numbers"
            if log != False: #Print to standard output as well
                print(new_addrNum)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addrNum + '\n')
            nf.close()
    def getStreet(self, mode=0, log=False):
        get = (self.addr).upper(); new_addr = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        if re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(STREET|STRE|STR|ST)(\W|$)", get): #Single char cardinal directions (STREET)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(STREET|STRE|STR|ST)(\W|$)", get)
            new_addr = self.getCompass(grab.group(1)) + ' ' + grab.group(2).strip(' ') + " STREET"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(STREET|STRE|STR|ST)(\W|$)", get): #All (STREET)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(STREET|STRE|STR|ST)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " STREET"

        elif re.search(r"(?!\d)(AVENUE|AVEN|AVE|AV|AE) ([A-Z])[ ,-]", get): #AVENUE [A-Z]
                    grab = re.search(r"(?!\d)(AVENUE|AVEN|AVE|AV|AE) ([A-Z])[ ,-]", get)
                    new_addr = "AVENUE " + grab.group(2)

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(AVENUE|AVEN|AVE|AV|AE)(\W|$)", get): #Single char cardinal directions (AVENUE)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(AVENUE|AVEN|AVE|AV|AE)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " AVENUE"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(AVENUE|AVEN|AVE|AV|AE)(\W|$)", get): #All (AVENUE)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(AVENUE|AVEN|AVE|AV|AE)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " AVENUE"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(ROAD|RD)(\W|$)", get): #Single char cardinal directions (ROAD)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(ROAD|RD)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " ROAD"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(ROAD|RD)(\W|$)", get): #All (ROAD)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(ROAD|RD)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " ROAD"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(DRIVE|DR)(\W|$)", get): #Single char cardinal directions (DRIVE)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(DRIVE|DR)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " DRIVE"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(DRIVE|DR)(\W|$)", get): #All (DRIVE)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(DRIVE|DR)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " DRIVE"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(PLACE|PLAC|PLCE|PL)(\W|$)", get): #Single char cardinal directions (PLACE)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(PLACE|PLAC|PLCE|PL)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " PLACE"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(PLACE|PLAC|PLCE|PL)(\W|$)", get): #All (PLACE)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(PLACE|PLAC|PLCE|PL)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " PLACE"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(BOULEVARD|BLVD|BOUL|BO)(\W|$)", get): #Single char cardinal directions (BOULEVARD)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(BOULEVARD|BLVD|BOUL|BO)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " BOULEVARD"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(BOULEVARD|BLVD|BOUL|BO)(\W|$)", get): #All (BOULEVARD)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(BOULEVARD|BLVD|BOUL|BO)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " BOULEVARD"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(LANE|LN)(\W|$)", get): #Single char cardinal directions (LANE)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(LANE|LN)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " LANE"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(LANE|LN)(\W|$)", get): #All (LANE)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(LANE|LN)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " LANE"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(COURT|CRT|CT)(\W|$)", get): #Single char cardinal directions (COURT)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(COURT|CRT|CT)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " COURT"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(COURT|CRT|CT)(\W|$)", get): #All (COURT)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(COURT|CRT|CT)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " COURT"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(HEIGHTS|HTS)(\W|$)", get): #Single char cardinal directions (HEIGHTS)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(HEIGHTS|HTS)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " HEIGHTS"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(HEIGHTS|HTS)(\W|$)", get): #All (HEIGHTS)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(HEIGHTS|HTS)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " HEIGHTS"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(PARKWAY|PKWY)(\W|$)", get): #Single char cardinal directions (PARKWAY)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(PARKWAY|PKWY)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " PARKWAY"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(PARKWAY|PKWY)(\W|$)", get): #All (PARKWAY)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(PARKWAY|PKWY)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " PARKWAY"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(HIGHWAY|HWAY|HWY)(\W|$)", get): #Single char cardinal directions (HIGHWAY)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(HIGHWAY|HWAY|HWY)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " HIGHWAY"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(HIGHWAY|HWAY|HWY)(\W|$)", get): #All (HIGHWAY)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(HIGHWAY|HWAY|HWY)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " HIGHWAY"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(EXPRESSWAY|EXPWA|EXPWY|EXPY|EXP)(\W|$)", get): #Single char cardinal directions (EXPRESSWAY)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(EXPRESSWAY|EXPWA|EXPWY|EXPY|EXP)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " EXPRESSWAY"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(EXPRESSWAY|EXPWA|EXPWY|EXPY|EXP)(\W|$)", get): #All (EXPRESSWAY)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(EXPRESSWAY|EXPWA|EXPWY|EXPY|EXP)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " EXPRESSWAY"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(BROADWAY|BDWY)(\W|$)", get): #Single char cardinal directions (BROADWAY)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(BROADWAY|BDWY)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " BROADWAY"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(BROADWAY|BDWY)(\W|$)", get): #All (BROADWAY)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(BROADWAY|BDWY)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " BROADWAY"

        elif re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(TURNPIKE|TPKE)(\W|$)", get): #Single char cardinal directions (TURNPIKE)
            grab = re.search(r"(?!\d) ([NSEW])( ?\d+ ?| [A-Z]+ )(TURNPIKE|TPKE)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " TURNPIKE"
        elif re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(TURNPIKE|TPKE)(\W|$)", get): #All (TURNPIKE)
            grab = re.search(r"(?!\d)( (NORTH |SOUTH |EAST |WEST )?\d+ ?| ([A-Z][A-Z]+ )+)(TURNPIKE|TPKE)(\W|$)", get)
            new_addr = grab.group(1).strip(' ') + " TURNPIKE"

        else:
            new_addr = "OTHER"
        if mode == 0:
            print(new_addr)
        else: #Write to new or specfied file
            fileName = re.sub(r"\..+", '', mode)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_addresses"
            if log != False: #Print to standard output as well
                print(new_addr)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr + '\n')
            nf.close()
    def getAddress(self):
        get = (self.addr).upper(); new_addr = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
