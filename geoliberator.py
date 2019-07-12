# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: GeoLiberator
Functionality Purpose: Instill data quality upon address data
Version: Alpha 0.2.0
'''
#7/12/19

import re
import sys
import time

##t0 = time.process_time_ns()

#Create load bar for autoGeoLiberate()
#Account for word house numbers
#Account for '331/River/NJ/Rd' and post cardinal direction
#Account for '&' and 'STS' and multiple street types
#Option to append borough, state, zip, based on argument
#Create custom address formatter

class AddressError(BaseException):
    pass

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
        self.states = {
            'Mississippi': 'MS', 'Oklahoma': 'OK', 'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
            'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 'Idaho': 'ID', 'Wyoming': 'WY',
            'Tennessee': 'TN', 'Arizona': 'AZ', 'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
            'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT', 'California': 'CA',
            'Massachusetts': 'MA', 'West Virginia': 'WV', 'South Carolina': 'SC', 'New Hampshire': 'NH',
            'Wisconsin': 'WI', 'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 'Pennsylvania': 'PA',
            'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY', 'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO',
            'Ohio': 'OH', 'Alabama': 'AL', 'New York': 'NY', 'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ',
            'Washington': 'WA', 'North Carolina': 'NC', 'District of Columbia': 'DC', 'Texas': 'TX', 'Nevada': 'NV',
            'Maine': 'ME', 'Rhode Island': 'RI'}
        self.streetTypes = {"ROAD": ["ROAD","RD","RO"],
                            "AVENUE": ["AVENUE","AVEN","AVE","AV","AE"],
                            "DRIVE": ["DRIVE","DRIV","DR"],
                            "PLACE": ["PLACE","PLAC","PLCE","PLC","PL"],
                            "BOULEVARD": ["BOULEVARD","BLVD","BOUL","BLV","BO"],
                            "COURT": ["COURT","CRT","CT"],
                            "HEIGHTS": ["HEIGHTS","HTS"],
                            "PARKWAY": ["PARKWAY","PKWAY","PKWY","PWAY","PWY","PKY"],
                            "HIGHWAY": ["HIGHWAY","HWAY","HWY"],
                            "EXPRESSWAY": ["EXPRESSWAY","EXPRESWY","EXPRESWAY","EXPREWAY","EXPWA","EXPWY","EXPY","EXWY","EWY","EXP"],
                            "PLAZA": ["PLAZA","PLAZ","PLZA","PLZ"],
                            "BRIDGE": ["BRIDGE","BRDG","BRG","BR"],
                            "CONCOURSE": ["CONCOURSE","CONC","CNCRS","CON","CO"],
                            "TERRACE": ["TERRACE","TERR","TER","TE"],
                            "CRESCENT": ["CRESCENT","CRESCNT","CRES"],
                            "ALLEY": ["ALLEY","ALY"], "GARDENS": ["GARDENS","GDNS"],
                            "ESPLANADE": ["ESPLANADE","ESPL"], "PARK": ["PARK","PRK","PK"],
                            "HILL": ["HILL","HL"], "LANE": ["LANE","LN"],
                            "PROMENADE": ["PROMENADE","PROM"], "COURSE": ["COURSE","CRSE"],
                            "FREEWAY": ["FREEWAY","FWY"], "TURNPIKE": ["TURNPIKE","TPKE"],
                            "SQUARE": ["SQUARE","SQ"], "CIRCLE": ["CIRCLE","CIR"],
                            "CLOSE": ["CLOSE","CLOS"], "VILLAGE": ["VILLAGE","VLG"],
                            "RIDGE": ["RIDGE","RDG"], "COVE": ["COVE","CV"],
                            "TRAIL": ["TRAIL","TRL"], "GREEN": ["GREEN","GRN"], "CAMP": ["CAMP","CP"],
                            "STREET": ["STREET","STRE","STR","ST"],
                            "SLIP": ["SLIP"],"LOOP": ["LOOP"], "WAY": ["WAY"],"EST": ["EST"],"ROW": ["ROW"],"OVAL": ["OVAL"],"PATH": ["PATH"]}
        self.wordTypes = ['ARCADIA', 'ATLANTIC', 'ATLANTIC COMMONS', 'BATH', 'BAYSIDE',
                          'BAYVIEW', 'BAYWAY', 'BCH RESERVATION', 'BOARDWALK',
                          'BOULEVARD', 'BOWERY', 'BRANT', 'BRIGHTON 1', 'BRIGHTON 2', 'BRIGHTON 3',
                          'BRIGHTON 4', 'BRIGHTON 7', 'BROADWAY ATRIUM', 'CENTRE MALL', 'CHESTER',
                          'CLINTON', 'CROSS BRONX EP SR', 'CROSS BRONX EP SR', 'CUMBERLAND', 'DEAUVILLE',
                          'DEVON', 'ESPLANADE', 'ESSEX', 'FLEET', 'FULTON', 'GOTHAM', 'GREENWAY', 'GREENWAY',
                          'GREENWICH MEWS', 'HAMILTON', 'HILLCREST', 'HUDSON', 'IRVING', 'JAMAICA', 'JONES',
                          'KILDARE', 'KINGSBOROUGH 2', 'KINGSBOROUGH 3', 'KINGSBOROUGH 4', 'KINGSBOROUGH 5',
                          'KINGSBOROUGH 6', 'KINGSBOROUGH 7', 'LAFAYETTE', 'LINCOLN', 'MARION', 'MONUMENT',
                          'ELLIOTT', 'OXFORD', 'NAVY', 'NEPTUNE', 'NEW ENGLAND THRUWAY', 'NEWPORT',
                          'NORTH RIVER PIERS', 'NORTHERN BL SR', 'OCEAN DRIVEWAY', 'OLIVE', 'PELHAM',
                          'PINEAPPLE', 'PLOUGHMANS BUSH', 'POMANDER', 'QUEENS MIDTOWN EP SR',
                          'QUEENS MIDTOWN EP SR', 'REGAL', 'ROOSEVELT', 'SEA BREEZE', 'STAGG', 'SUFFOLK',
                          'TEN EYCK', 'UTICA', 'WASHINGTON', 'WASHINGTON MEWS', {'BROADWAY': ['BROADWAY','BRDWY','BDWY','BWAY','BWY']}]
        hold = ''
        for typ in self.streetTypes:
            hold += re.sub(r"[\[\]' ]", '', str(self.streetTypes[typ])) + ','
        self.streetTypesAll = list(hold.strip(',').split(','))

    def getCompass(self, direc):
        if 'N' == direc or "NO" == direc:
            return "NORTH"
        elif 'S' == direc or "SO" == direc:
            return "SOUTH"
        elif 'E' == direc:
            return "EAST"
        elif 'W' == direc:
            return "WEST"
        else:
            return False

    def ordinalAdd(self, num):
        nn = ''
        if re.search(r"(?<!1)1$", num):
            nn = num + 'st'
        elif num[-1] == '2':
            nn = num + 'nd'
        elif num[-1] == '3':
            nn = num + 'rd'
        else:
            nn = num + 'th'
        return nn

    def searchCycle(self, g, sF):
        new_find = ''
        if sF == False:
            for stre in self.wordTypes: #Check for word/name street types
                getStreet = re.search(fr"(?!\d)?(\W|^)({stre})(\W|$)", g)
                if type(stre) == dict:
                    streB = '|'.join(stre['BROADWAY'])
                    if re.search(fr"(?!\d)?\W?({streB})(\W|$)", g):
                        new_find = "BROADWAY"
                        break
                if getStreet:
                    new_find = getStreet.group(2)
                    break
        for key, val in self.streetTypes.items():
            if new_find != '':
                break
            sType = '|'.join(val)
            getStreetPattern1 = re.search(fr"(?!\d)?(\W|^|\d)([NSEW]|NO|SO)(\.? ?\d+(ST)? ?|(\. ?| )([A-Z]+ )+)({sType})\.?(?=\W|$)", g)
            getStreetPattern2 = re.search(fr"(?!\d)?( ?(NORTH |SOUTH |EAST |WEST )?[^\W]?\d+(ST)? ?|([A-Z]+ )+)({sType})\.?((?=\W)|$)", g)
            getStreetPattern3 = re.search(r"(?!\d)?(AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$)", g)
            if getStreetPattern1:
                if getStreetPattern1.group(4) in self.streetTypes[key] or getStreetPattern1.group(7) in self.streetTypes[key]:
                    new_find = self.getCompass(getStreetPattern1.group(2)) + ' ' + getStreetPattern1.group(3).strip('. ') + f" {key}"
                    break
            elif getStreetPattern2:
                if getStreetPattern2.group(3) in self.streetTypes[key] or getStreetPattern2.group(5) in self.streetTypes[key]:
                    new_find = getStreetPattern2.group(1).strip(' ') + f" {key}"
                    break
            elif getStreetPattern3: #IMPLEMENT CARDINAL DIRECTIONS
                new_find = "AVENUE " + getStreetPattern3.group(2)
                break
        if sF == True and new_find != '':
            new_find = "SAINT " + str(new_find)
        if new_find == '':
            new_find = "OTHER"
        return new_find

    def getAddressNum(self, log='', mode=False):
        get = (self.addr).upper(); new_addr_num = '' #Uppercase and create new address to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for key, val in self.streetTypes.items():
            sType = '|'.join(val)
            group1 = fr"(^\d+([- ]\d+)?)(?=[NSEW]\.? ?\d+ ?(ST)\.?(\W|$))"
            group2 = fr"(^\d+([- ]\d+)?)(?= ((\w+\.? ?)+)({sType})\.?(\W|$))"
            group3 = r"(?=\d+([ -]\d+)? (AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$))^\d+([- ]\d+)?"
            gANpat1 = re.search(fr"{group1}|{group2}", get)
            gANpat2 = re.search(fr"{group3}", get)
            if gANpat1:
                new_addr_num = gANpat1.group().replace(' ', '-')
            elif gANpat2:
                new_addr_num = gANpat2.group().replace(' ', '-')
        if new_addr_num == '':
            new_addr_num = "OTHER"

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
        return str(new_addr_num)

    def getStreet(self, log='', mode=False):
        get = (self.addr).upper(); new_street = ''; saintFlag = False #Uppercase and create new address to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        if re.search(r"(\W|^)(ST|SNT)\W", get): #Check for 'Saint'
            get1 = re.sub(r"(\W|^)(ST|SNT)\W", ' ', get)
            saintFlag = True
            new_street = self.searchCycle(get1, saintFlag)
            if new_street == "OTHER":
                saintFlag = False
                new_street = self.searchCycle(get, saintFlag)
        else:
            new_street = self.searchCycle(get, saintFlag)
        new_street = re.sub(r"^FT\W| FT\W", "FORT ", new_street) #Replace 'FT' with 'FORT'
        new_street = re.sub(r"(?<=1)ST", '', new_street) #Strip 1st ordinal number
        if re.search(r"\d+", new_street): #Apply ordinal numbers
            ordNum = self.ordinalAdd(str(re.search(r"\d+", new_street).group()))
            new_street = re.sub(r"\d+", ordNum, new_street)

        if log == '' and mode == True: #Print to standard output and return value
            print(new_street)
        elif log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_streets"
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

#Acount the lines in a file
def file_len(file_name):
    with open(file_name) as f:
        for i, L in enumerate(f):
            pass
    return i + 1

#Takes text file as input and switch argument to determine which address property to be standardized
def autoGeoLiberate(file_path, switch=2, write=''):
    mode = True
    if write != '':
        mode = False
    with open(file_path) as f:
        lines = f.readlines()
        if len(sys.argv) == 2:
            if sys.argv[1] == '--status' or sys.argv[1] == "-S":
                FL = file_len(file_path)
                barIncr = int(FL * .025); barNum = 0; dashNum = 40; c = 0; lc = 0
                for line in lines:
                    perc = (lc/FL)
                    bar = '|' + ('█' * barNum) + ('-' * dashNum) + '|' + " [{:>.2%}]".format(perc)
                    c += 1; lc += 1
                    if c == barIncr:
                       if barNum < 39:
                           c = 0; barNum += 1; dashNum -= 1
                           print(f"\r{bar}", end=''); sys.stdout.flush()
                    elif lc == FL:
                       print('\r|' + ('█' * 40) + '|' + " [100%]  "); sys.stdout.flush()
                    adr = GeoLiberator(str(line))
                    if switch == 2:
                        adr.getAddress(log=write, mode=mode)
                    elif switch == 1:
                        adr.getAddressNum(log=write, mode=mode)
                    elif switch == 0:
                        adr.getStreet(log=write, mode=mode)
        else:
            if mode == False:
                print("Running...")
            for line in lines:
                adr = GeoLiberator(str(line))
                if switch == 2:
                    adr.getAddress(log=write, mode=mode)
                elif switch == 1:
                    adr.getAddressNum(log=write, mode=mode)
                elif switch == 0:
                    adr.getStreet(log=write, mode=mode)
            print("Done!")

#Takes address as input and switch argument to determine which address property to be standardized
def geoLiberate(addr, switch=2):
    adr = GeoLiberator(str(addr))
    if switch == 2:
        adr.getAddress(mode=True)
    elif switch == 1:
        adr.getAddressNum(mode=True)
    elif switch == 0:
        adr.getStreet(mode=True)

##t1 = time.process_time_ns()
##total = t1 - t0
##if __name__ == "__main__":
##    print(f"Timestamp 1: {t0} n/s\nTimestamp 2: {t1} n/s")
##    print("Module Time Elapsed:", total, "nanoseconds")
