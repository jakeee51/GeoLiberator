import pandas as pd
import re
import time
t0 = time.process_time_ns()

#Account for '&' and Saint(ST) and Fort(FT)
#Create full address parser
#Clear further to pick up missed matches
#Attempt to optimize speed by looping through streetTypes["All"] while executing re.search(fr"...{}...")

class AddressError(BaseException):
    pass

class GeoLiberator:
    '''
    A class for instantiating governance & uniformity on full addresses

    GeoLiberator class takes in entire address as first argument and returns the instantiated GeoLiberator Object.
    One may manipulate object using member functions in order to parse certain properties of the address.
    Second 'mode' argument set to 'print' by default to print to standard output or write to new specified file name.
    '''
    streetTypes = {"All": ["STREET","STRE","STR","ST",
                           "AVENUE","AVEN","AVE","AV","AE",
                           "ROAD","RD","DRIVE","DR",
                           "PLACE","PLAC","PLCE","PL","PLC",
                           "BOULEVARD","BLVD","BOUL","BO",
                           "LANE","LN","COURT","CRT","CT",
                           "HEIGHTS","HTS","PARKWAY","PKWY",
                           "HIGHWAY","HWAY","HWY",
                           "EXPRESSWAY","EXPWA","EXPWY","EXPY","EXP",
                           "BROADWAY","BDWY","BWY","TURNPIKE","TPKE"],
                   "STREET": ["STREET","STRE","STR","ST"],
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
        strPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(STREET|STRE\.?|STR\.?|ST\.?)(\W|$)", get) #STREET
        strPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(STREET|STRE\.?|STR\.?|ST\.?)(\W|$)", get)
        avePat1 = re.search(r"(?!\d)(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z])[ ,-]", get) #AVENUE
        avePat2 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?)(\W|$)", get)
        avePat3 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?)(\W|$)", get)
        rdPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(ROAD|RD\.?)(\W|$)", get) #ROAD
        rdPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(ROAD|RD\.?)(\W|$)", get)
        drvPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(DRIVE|DR\.?)(\W|$)", get) #DRIVE
        drvPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(DRIVE|DR\.?)(\W|$)", get)
        plcPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(PLACE|PLAC\.?|PLCE\.?|PL\.?|PLC\.?)(\W|$)", get) #PLACE
        plcPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(PLACE|PLAC\.?|PLCE\.?|PL\.?|PLC\.?)(\W|$)", get)
        blvdPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(BOULEVARD|BLVD\.?|BOUL\.?|BO\.?)(\W|$)", get) #BOULEVARD
        blvdPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(BOULEVARD|BLVD\.?|BOUL\.?|BO\.?)(\W|$)", get)
        lnPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(LANE|LN\.?)(\W|$)", get) #LANE
        lnPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(LANE|LN\.?)(\W|$)", get)
        crtPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(COURT|CRT\.?|CT\.?)(\W|$)", get) #COURT
        crtPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(COURT|CRT\.?|CT\.?)(\W|$)", get)
        htsPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(HEIGHTS|HTS\.?)(\W|$)", get) #HEIGHTS
        htsPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(HEIGHTS|HTS\.?)(\W|$)", get)
        pwyPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(PARKWAY|PKWY\.?)(\W|$)", get) #PARKWAY
        pwyPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(PARKWAY|PKWY\.?)(\W|$)", get)
        hwyPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(HIGHWAY|HWAY\.?|HWY\.?)(\W|$)", get) #HIGHWAY
        hwyPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(HIGHWAY|HWAY\.?|HWY\.?)(\W|$)", get)
        expPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(EXPRESSWAY|EXPWA\.?|EXPWY\.?|EXPY\.?|EXP\.?)(\W|$)", get) #EXPRESWAY
        expPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(EXPRESSWAY|EXPWA\.?|EXPWY\.?|EXPY\.?|EXP\.?)(\W|$)", get)
        bwyPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(BROADWAY|BDWY\.?|BWY\.?)(\W|$)", get) #BROADWAY
        bwyPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(BROADWAY|BDWY\.?|BWY\.?)(\W|$)", get)
        tpkPat1 = re.search(r"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )(TURNPIKE|TPKE\.?)(\W|$)", get) #TURNPIKE
        tpkPat2 = re.search(r"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)(TURNPIKE|TPKE\.?)(\W|$)", get)
        if strPat1: #Single char cardinal directions (STREET)
            grab = strPat1
            new_addr = self.getCompass(grab.group(1)) + ' ' + grab.group(2).strip(' ') + " STREET"
        elif strPat2: #All (STREET)
            grab = strPat2
            new_addr = grab.group(1).strip(' ') + " STREET"

        elif avePat1: #AVENUE [A-Z]
                    grab = avePat1
                    new_addr = "AVENUE " + grab.group(2)
        elif avePat2: #Single char cardinal directions (AVENUE)
            grab = avePat2
            new_addr = grab.group(1).strip(' ') + " AVENUE"
        elif avePat3: #All (AVENUE)
            grab = avePat3
            new_addr = grab.group(1).strip(' ') + " AVENUE"

        elif rdPat1: #Single char cardinal directions (ROAD)
            grab = rdPat1
            new_addr = grab.group(1).strip(' ') + " ROAD"
        elif rdPat2: #All (ROAD)
            grab = rdPat2
            new_addr = grab.group(1).strip(' ') + " ROAD"

        elif drvPat1: #Single char cardinal directions (DRIVE)
            grab = drvPat1
            new_addr = grab.group(1).strip(' ') + " DRIVE"
        elif drvPat2: #All (DRIVE)
            grab = drvPat2
            new_addr = grab.group(1).strip(' ') + " DRIVE"

        elif plcPat1: #Single char cardinal directions (PLACE)
            grab = plcPat1
            new_addr = grab.group(1).strip(' ') + " PLACE"
        elif plcPat2: #All (PLACE)
            grab = plcPat2
            new_addr = grab.group(1).strip(' ') + " PLACE"

        elif blvdPat1: #Single char cardinal directions (BOULEVARD)
            grab = blvdPat1
            new_addr = grab.group(1).strip(' ') + " BOULEVARD"
        elif blvdPat2: #All (BOULEVARD)
            grab = blvdPat2
            new_addr = grab.group(1).strip(' ') + " BOULEVARD"

        elif lnPat1: #Single char cardinal directions (LANE)
            grab = lnPat1
            new_addr = grab.group(1).strip(' ') + " LANE"
        elif lnPat2: #All (LANE)
            grab = lnPat2
            new_addr = grab.group(1).strip(' ') + " LANE"

        elif crtPat1: #Single char cardinal directions (COURT)
            grab = crtPat1
            new_addr = grab.group(1).strip(' ') + " COURT"
        elif crtPat2: #All (COURT)
            grab = crtPat2
            new_addr = grab.group(1).strip(' ') + " COURT"

        elif htsPat1: #Single char cardinal directions (HEIGHTS)
            grab = htsPat1
            new_addr = grab.group(1).strip(' ') + " HEIGHTS"
        elif htsPat2: #All (HEIGHTS)
            grab = htsPat2
            new_addr = grab.group(1).strip(' ') + " HEIGHTS"

        elif pwyPat1: #Single char cardinal directions (PARKWAY)
            grab = pwyPat1
            new_addr = grab.group(1).strip(' ') + " PARKWAY"
        elif pwyPat2: #All (PARKWAY)
            grab = pwyPat2
            new_addr = grab.group(1).strip(' ') + " PARKWAY"

        elif hwyPat1: #Single char cardinal directions (HIGHWAY)
            grab = hwyPat1
            new_addr = grab.group(1).strip(' ') + " HIGHWAY"
        elif hwyPat2: #All (HIGHWAY)
            grab = hwyPat2
            new_addr = grab.group(1).strip(' ') + " HIGHWAY"

        elif expPat1: #Single char cardinal directions (EXPRESSWAY)
            grab = expPat1
            new_addr = grab.group(1).strip(' ') + " EXPRESSWAY"
        elif expPat2: #All (EXPRESSWAY)
            grab = expPat2
            new_addr = grab.group(1).strip(' ') + " EXPRESSWAY"

        elif bwyPat1: #Single char cardinal directions (BROADWAY)
            grab = bwyPat1
            new_addr = grab.group(1).strip(' ') + " BROADWAY"
        elif bwyPat2: #All (BROADWAY)
            grab = bwyPat2
            new_addr = grab.group(1).strip(' ') + " BROADWAY"

        elif tpkPat1: #Single char cardinal directions (TURNPIKE)
            grab = tpkPat1
            new_addr = grab.group(1).strip(' ') + " TURNPIKE"
        elif tpkPat2: #All (TURNPIKE)
            grab = tpkPat2
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
t1 = time.process_time_ns()
total = t1 - t0
if __name__ != "__main__":
    print(f"Timestamp 1: {t0} n/s\nTimestamp 2: {t1} n/s")
    print("Time elapsed:", total, "nanoseconds")
