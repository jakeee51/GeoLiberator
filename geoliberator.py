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
    def getStreet(self, mode=0, log=False):
        get = (self.addr).upper(); new_addr = ''
        get = (re.sub(r"[!#$%^*+=`~/]", ' ', get)).strip(' ')
        try:
            if re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(ST|STR|STRE|STREET)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(ST|STR|STRE|STREET)\W?", get)
                if grab.group(1).strip(' ').isdigit():
                    new_addr = grab.group(1).strip(' ') + ' STREET'
                else:
                    new_addr = grab.group(4)
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(AV|AE|AVE|AVEN|AVENUE)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(AV|AE|AVE|AVEN|AVENUE)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' AVENUE'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(RD|ROAD)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(RD|ROAD)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' ROAD'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(DR|DRIVE)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(DR|DRIVE)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' DRIVE'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PL|PLCE|PLAC|PLACE)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PL|PLCE|PLAC|PLACE)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' PLACE'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BO|BLVD|BOUL|BOULEVARD)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BO|BLVD|BOUL|BOULEVARD)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' BOULEVARD'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PKWY|PARKWAY)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(PKWY|PARKWAY)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' PARKWAY'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HWY|HWAY|HIGHWAY)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HWY|HWAY|HIGHWAY)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' HIGHWAY'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(EXP|EXPY|EXPWY|EXPWA|EXPRESSWAY)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(EXP|EXPY|EXPWY|EXPWA|EXPRESSWAY)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' EXPRESSWAY'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BDWY|BROADWAY)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(BDWY|BROADWAY)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' BROADWAY'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(LANE)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(LANE)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' LANE'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(CT|CRT|COURT)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(CT|CRT|COURT)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' COURT'
            elif re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HTS|HEIGHTS)\W?", get):
                grab = re.search(r"((?!\d)\W(\w+ )+)?(\w+(\W|\d))(HTS|HEIGHTS)\W?", get)
                new_addr = grab.group(1).strip(' ') + ' HEIGHTS'
            else:
                new_addr = "OTHER"
                raise AddressError
        except AddressError:
            assert 0 == "{cause}", "{reason}"
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

adr = GeoLiberator("331 2 Street")
adr.getStreet()
##with open("hold.txt") as f:
##    lines = f.readlines()
##    for line in lines:
##        adr = GeoLiberator(str(line))
##        adr.getStreet("addresses_output_log")
