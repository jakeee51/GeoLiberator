import pandas as pd
import re

#Create full street parser
#Analyze specParse for '-' & 'norm'
#Create full address parser
#Clear further to pick up mismatches
#Gain even more string matches

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
    def getAddressNum(self):
        pass
    def getStreet(self, mode=0):
        get = (self.addr).upper(); new_addr = ''
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ')
        if re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(STREET|STRE|STR|ST)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(STREET|STRE|STR|ST)\W?", get)
            if re.sub(r"(\D+)", '', grab.group(3)).isdigit():
                new_addr = re.sub(r"(\D+)", '', grab.group(3)) + ' STREET'
            else:
                if grab.group(1) == None:
                    new_addr = grab.group(3) + 'STREET'
                else:
                    new_addr = ''.join(grab.group(1,2,3)) + 'STREET'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(AVENUE|AVEN|AVE|AV|AE)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(AVENUE|AVEN|AVE|AV|AE)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' AVENUE'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(ROAD|RD)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(ROAD|RD)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' ROAD'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(DRIVE|DR)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(DRIVE|DR)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' DRIVE'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PLACE|PLAC|PLCE|PL)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PLACE|PLAC|PLCE|PL)\W", get)
            new_addr = grab.group(1).strip(' ') + ' PLACE'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BOULEVARD|BLVD|BOUL|BO)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BOULEVARD|BLVD|BOUL|BO)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' BOULEVARD'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PARKWAY|PKWY)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PARKWAY|PKWY)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' PARKWAY'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HIGHWAY|HWAY|HWY|)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HIGHWAY|HWAY|HWY|)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' HIGHWAY'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(EXPRESSWAY|EXPWA|EXPWY|EXPY|EXP)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(EXPRESSWAY|EXPWA|EXPWY|EXPY|EXP)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' EXPRESSWAY'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BROADWAY|BDWY)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BROADWAY|BDWY)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' BROADWAY'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(LANE|LN)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(LANE|LN)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' LANE'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(COURT|CRT|CT)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(COURT|CRT|CT)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' COURT'
        elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HEIGHTS|HTS)\W?", get):
            grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HEIGHTS|HTS)\W?", get)
            new_addr = grab.group(1).strip(' ') + ' HEIGHTS'
        else:
            new_addr = "OTHER"
        if mode == 0:
            print(new_addr)
        else: #Write to new or specfied file
            fileName = re.sub(r"\..+", '', mode)
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr + '\n')
            nf.close()
    def getAddress(self):
        get = (self.addr).upper()
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ')

adr = GeoLiberator("331 Martin Luther King Jr Street")
adr.getStreet()
##with open("hold.txt") as f:
##    lines = f.readlines()
##    for line in lines:
##        adr = GeoLiberator(str(line))
##        adr.getStreet("addresses_output_log")
