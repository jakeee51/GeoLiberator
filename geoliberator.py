import pandas as pd
import re
import time
t0 = time.process_time_ns()

#Account for '&' and Saint(ST) and Fort(FT)
#Create full address parser

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
        self.streetTypesAll = ["STREET","STRE","STR","ST",
                   "AVENUE","AVEN","AVE","AV","AE",
                   "ROAD","RD","DRIVE","DR",
                   "PLACE","PLAC","PLCE","PL","PLC",
                   "BOULEVARD","BLVD","BOUL","BO",
                   "LANE","LN","COURT","CRT","CT",
                   "HEIGHTS","HTS","PARKWAY","PKWY",
                   "HIGHWAY","HWAY","HWY",
                   "EXPRESSWAY","EXPWA","EXPWY","EXPY","EXP",
                   "BROADWAY","BDWY","BWY","TURNPIKE","TPKE", 0]
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
                            "TURNPIKE": ["TURNPIKE","TPKE"],
                            "***END***": [0]}
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
        get = (self.addr).upper(); new_addr_num = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for sType in self.streetTypesAll:
            if sType == 0 and new_addr_num == '':
                new_addr_num = "OTHER"
                break
            elif new_addr_num != '':
                break
            if re.search(fr"(^\d+(-\d+)?) (?!({sType}\.?))", get):
                grab = re.search(fr"(^\d+(-\d+)?) (?!({sType}\.?))", get)
                new_addr_num = grab.group(1)
        if mode == 0 and log = True:
            print(new_addr_num)
            return new_addr_num
        else: #Write to new or specfied file
            fileName = re.sub(r"\..+", '', mode)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_address_numbers"
            if log != False: #Print to standard output as well
                print(new_addr_num)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr_num + '\n')
            nf.close()
            return new_addr_num
    def getStreet(self, mode=0, log=False):
        get = (self.addr).upper(); new_addr = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for key in self.streetTypes:
            if key == "***END***" and new_addr == '':
                new_addr = "OTHER"
                break
            for sType in self.streetTypes[key]:
                pat1 = re.search(fr"(?!\d)([NSEW])( ?\d+ ?| [A-Z]+ )({sType}\.?)(\W|$)", get)
                pat2 = re.search(fr"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?\d+ ?|([A-Z][A-Z]+ )+)({sType}\.?)((?=\W)|$)", get)
                pat3 = re.search(fr"(?!\d)(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z])[ ,-]", get)
                if pat1:
                    if pat1.group(3) in self.streetTypes[key]:
                        new_addr = self.getCompass(pat1.group(1)) + ' ' + pat1.group(2).strip(' ') + f" {key}"
                elif pat2:
                    if pat2.group(4) in self.streetTypes[key]:
                        new_addr = pat2.group(1).strip(' ') + f" {key}"
                elif pat3:
                    new_addr = "AVENUE " + pat3.group(2)
                else:
                    continue
        if mode == 0 and log == True:
            print(new_addr)
            return new_addr
        else: #Write to new or specfied file
            fileName = re.sub(r"\..+", '', mode)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_addresses"
            if log != False: #Print to standard output as well
                print(new_addr)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr + '\n')
            nf.close()
            return new_addr
    def getAddress(self):
        get = (self.addr).upper(); new_addr = '' #Uppercase and create new address to return
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers

t1 = time.process_time_ns()
total = t1 - t0
if __name__ == "__main__":
    print(f"Timestamp 1: {t0} n/s\nTimestamp 2: {t1} n/s")
    print("Module Time Elapsed:", total, "nanoseconds")
