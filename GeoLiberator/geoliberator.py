# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: GeoLiberator
Functionality Purpose: Instill data quality upon address data
Version: Alpha 0.2.1
'''
#7/15/19

import re
import sys
import time

##t0 = time.process_time_ns()

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
        self.states = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
                       "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
                       "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
                       "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
                       "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
                       "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
                       "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
                       "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
                       "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
                       "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
                       "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
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
                            "PARK": ["PARK","PRK","PK"],
                            "HILL": ["HILL","HL"], "LANE": ["LANE","LN"],
                            "PROMENADE": ["PROMENADE","PROM"], "COURSE": ["COURSE","CRSE"],
                            "FREEWAY": ["FREEWAY","FWY"], "TURNPIKE": ["TURNPIKE","TPKE"],
                            "SQUARE": ["SQUARE","SQ"], "CIRCLE": ["CIRCLE","CIR"],
                            "CLOSE": ["CLOSE","CLOS"], "VILLAGE": ["VILLAGE","VLG"],
                            "RIDGE": ["RIDGE","RDG"], "COVE": ["COVE","CV"],
                            "TRAIL": ["TRAIL","TRL"], "GREEN": ["GREEN","GRN"], "CAMP": ["CAMP","CP"],
                            "STREET": ["STREET","STREE","STRE","STR","ST"],
                            "SLIP": ["SLIP"],"LOOP": ["LOOP"], "WAY": ["WAY"],"EST": ["EST"],"ROW": ["ROW"],"OVAL": ["OVAL"],"PATH": ["PATH"]}
        self.wordTypes = ['ARCADIA', 'ATLANTIC', 'ATLANTIC COMMONS', 'BATH', 'BAYSIDE',
                          'BAYVIEW', 'BAYWAY', 'BCH RESERVATION', 'BOARDWALK',
                          'BOULEVARD', 'BOWERY', 'BRANT', 'BRIGHTON 1', 'BRIGHTON 2', 'BRIGHTON 3',
                          'BRIGHTON 4', 'BRIGHTON 7', 'BROADWAY ATRIUM', 'CENTRE MALL', 'CHESTER',
                          'CLINTON', 'CROSS BRONX EP SR', 'CROSS BRONX EP SR', 'CUMBERLAND', 'DEAUVILLE',
                          'DEVON', 'ESSEX', 'FLEET', 'FULTON', 'GOTHAM', 'GREENWAY', 'GREENWAY',
                          'GREENWICH MEWS', 'HAMILTON', 'HILLCREST', 'HUDSON', 'IRVING', 'JAMAICA', 'JONES',
                          'KILDARE', 'KINGSBOROUGH 2', 'KINGSBOROUGH 3', 'KINGSBOROUGH 4', 'KINGSBOROUGH 5',
                          'KINGSBOROUGH 6', 'KINGSBOROUGH 7', 'LAFAYETTE', 'LINCOLN', 'MARION', 'MONUMENT',
                          'ELLIOTT', 'OXFORD', 'NAVY', 'NEPTUNE', 'NEW ENGLAND THRUWAY', 'NEWPORT',
                          'NORTH RIVER PIERS', 'NORTHERN BL SR', 'OCEAN DRIVEWAY', 'OLIVE', 'PELHAM',
                          'PINEAPPLE', 'PLOUGHMANS BUSH', 'POMANDER', 'QUEENS MIDTOWN EP SR',
                          'QUEENS MIDTOWN EP SR', 'REGAL', 'ROOSEVELT', 'SEA BREEZE', 'STAGG', 'SUFFOLK',
                          'TEN EYCK', 'UTICA', 'WASHINGTON', 'WASHINGTON MEWS',
                          {"ESPLANADE": ["ESPLANADE","ESPL"], 'BROADWAY': ['BROADWAY','BRDWY','BDWY','BWAY','BWY']}]
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
                    streA = '|'.join(stre["ESPLANADE"])
                    streB = '|'.join(stre["BROADWAY"])
                    if re.search(fr"(?!\d)?\W?({streA})(\W|$)", g):
                        new_find = "ESPLANADE"
                        break
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

    def getAddressNum(self, log=''):
        get = (self.addr).upper(); new_addr_num = '' #Uppercase and create new address to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        for val in self.wordTypes:
            if type(val) == dict:
                streA = '|'.join(val["ESPLANADE"])
                streB = '|'.join(val["BROADWAY"])
                grab = re.search(fr"(?!\d)?\W?({streA}|{streB})(\W|$)", get); wType = ''
                if grab:
                    wType = grab.group(1)
                group1 = fr"(^\d+([- ]\d+)?)(?=[NSEW]\.? ?\d+ ?({wType})\.?(\W|$))"
                group2 = fr"(^\d+([- ]\d+)?)(?= ((\w+\.? ?)+)({wType})\.?(\W|$))"
                group3 = r"(?=\d+([ -]\d+)? (AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$))^\d+([- ]\d+)?"
                gANpat1 = re.search(fr"{group1}|{group2}", get)
                gANpat2 = re.search(fr"{group3}", get)
                if gANpat1:
                    new_addr_num = gANpat1.group().replace(' ', '-')
                elif gANpat2:
                    new_addr_num = gANpat2.group().replace(' ', '-')
            else:
                sType = '|'.join(val)
                group1 = fr"(^\d+([- ]\d+)?)(?=[NSEW]\.? ?\d+ ?({sType})\.?(\W|$))"
                group2 = fr"(^\d+([- ]\d+)?)(?= ((\w+\.? ?)+)({sType})\.?(\W|$))"
                group3 = r"(?=\d+([ -]\d+)? (AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$))^\d+([- ]\d+)?"
                gANpat1 = re.search(fr"{group1}|{group2}", get)
                gANpat2 = re.search(fr"{group3}", get)
                if gANpat1:
                    new_addr_num = gANpat1.group().replace(' ', '-')
                elif gANpat2:
                    new_addr_num = gANpat2.group().replace(' ', '-')
        for key, val in self.streetTypes.items():
            sType = '|'.join(val)
            group1 = fr"(^\d+([- ]\d+)?)(?=[NSEW]\.? ?\d+ ?({sType})\.?(\W|$))"
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

        if log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_address_numbers"
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_addr_num + '\n')
            nf.close()
        return str(new_addr_num)

    def getStreet(self, log=''):
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

        if log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_streets"
            nf = open(f"{fileName}.txt", 'a')
            nf.write(new_street + '\n')
            nf.close()
        return new_street

    def getAddress(self, log=''):
        get = (self.addr).upper(); new_addr = '' #Uppercase and create new address to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]| +", ' ', get)).strip(' ') #Strip any anomalies
        get = re.sub(r"(?<=\d)(ND|RD|TH|RTH)", '', get) #Strip any char of ordinal numbers
        gS = GeoLiberator(get).getStreet()
        gAN = GeoLiberator(get).getAddressNum()
        if gAN != "OTHER" and gS != "OTHER":
            new_addr = gAN + ' ' + gS
        else:
            new_addr = "OTHER"

        if log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName == '' or fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_addresses"
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
def autoGeoLiberate(file_path, parse="address", write=''):
    mode = True
    if write != '':
        mode = False
    with open(file_path) as f:
        lines = f.readlines()
        if len(sys.argv) == 2 and write != '':
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
                    if parse.lower() == "address":
                        adr.getAddress(log=write)
                    elif parse.lower() == "number":
                        adr.getAddressNum(log=write)
                    elif parse.lower() == "street":
                        adr.getStreet(log=write)
        else:
            if mode == False:
                print("Running...")
            for line in lines:
                adr = GeoLiberator(str(line))
                if parse.lower() == "address":
                    out = adr.getAddress(log=write)
                elif parse.lower() == "number":
                    out = adr.getAddressNum(log=write)
                elif parse.lower() == "street":
                    out = adr.getStreet(log=write)
                if mode == True:
                    print(out)
            print("Done!")

#Takes address as input and switch argument to determine which address property to be standardized
def geoLiberate(addr, parse="address"):
    adr = GeoLiberator(str(addr))
    if parse.lower() == "address":
        adr.getAddress()
    elif parse.lower() == "number":
        adr.getAddressNum()
    elif parse.lower() == "street":
        adr.getStreet()

##t1 = time.process_time_ns()
##total = t1 - t0
##if __name__ == "__main__":
##    print(f"Timestamp 1: {t0} n/s\nTimestamp 2: {t1} n/s")
##    print("Module Time Elapsed:", total, "nanoseconds")
