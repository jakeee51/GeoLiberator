# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: GeoLiberator
Functionality Purpose: Instill data quality upon address data
Version: Beta
'''
#8/6/20

import re
import sys
import time
import pandas as pd

#Account for post cardinal direction
#Account for '&' and 'STS' and multiple street types
#Create custom address formatter

#Options to return Street Type, Cardinal Direction
#Implement __main__.py for cli tools (use argparse)
 #https://realpython.com/command-line-interfaces-python-argparse/
#Function to parse city
#Allow street types, wordTypes & Cities to be appended to library or option to use one's own library

reason = ["Invalid parse argument given", "File type not supported", "Use 'address_field' argument for csv & excel files"]

class AddressError(BaseException):
    pass

class ArgumentError(Exception):
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
        GL_Object.getAddress(log="output_log.txt") #This code appends parsed address to a log file (useful in loops)
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
        self.streetTypes = {"HEIGHTS": ["HEIGHTS","HTS"],
                            "ROAD": ["ROAD","RD","RO"],
                            "AVENUE": ["AVENUE","AVEN","AVE","AV","AE"],
                            "DRIVE": ["DRIVE","DRIV","DR"],
                            "PLACE": ["PLACE","PLAC","PLCE","PLC","PL"],
                            "BOULEVARD": ["BOULEVARD","BLVD","BOUL","BLV","BO"],
                            "COURT": ["COURT","CRT","CT"],
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
    def __none_other(self, *args):
        for val in args:
            if val == "OTHER":
                return False
        return True

    def _get_compass(self, direc):
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

    def _ordinal_add(self, num):
        nn = ''
        if num == '11' or num == '12' or num == '13':
            return num + 'th'
        if re.search(r"(?<!1)1$", num):
            nn = num + 'st'
        elif num[-1] == '2':
            nn = num + 'nd'
        elif num[-1] == '3':
            nn = num + 'rd'
        else:
            nn = num + 'th'
        return nn

    def _search_cycle(self, g, sF):
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
                    new_find = self._get_compass(getStreetPattern1.group(2)) + ' ' + getStreetPattern1.group(3).strip('. ') + f" {key}"
                    break
            elif getStreetPattern2:
                if getStreetPattern2.group(3) in self.streetTypes[key] or getStreetPattern2.group(5) in self.streetTypes[key]:
                    new_find = getStreetPattern2.group(1).strip(' ') + f" {key}"
                    break
            elif getStreetPattern3: #IMPLEMENT CARDINAL DIRECTIONS
                new_find = "AVENUE " + getStreetPattern3.group(2)
                break
        if sF == True and new_find != '':
            cardir = re.search(r"(NORTH|SOUTH|EAST|WEST) ", str(new_find))
            if cardir:
                new_find = re.sub(fr"{cardir[1]} ", f"{cardir[1]} SAINT ", new_find)
            else:
                new_find = "SAINT " + str(new_find)
        if new_find == '':
            new_find = "OTHER"
        return new_find

    def get_zip(self, log=''):
        get = (self.addr).upper(); full_zip = '' #Uppercase and create get zipcode to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
        if re.search(r"\b\d{5}\b", get):
            full_zip = re.search(r"\b\d{5}\b", get).group()
        else:
            full_zip = "OTHER"

        if log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_zipcodes"
            nf = open(f"{fileName}.txt", 'a')
            nf.write(full_zip + '\n')
            nf.close()
        return full_zip

    def get_state(self, log=''):
        get = (self.addr).upper(); full_state = '' #Uppercase and find full state to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
        for key, val in self.states.items():
            if re.search(fr"\b{val}\b", get):
                full_state = key
        if full_state == '':
            full_state = "OTHER"

        if log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_states"
            nf = open(f"{fileName}.txt", 'a')
            nf.write(full_state + '\n')
            nf.close()
        return str(full_state).upper()

    def getAddressNum(self, log=''):
        get = (self.addr).upper(); new_addr_num = '' #Uppercase and create get house number to return
        if not get[0].isdigit():
            for key, val in self.states.items():
                if re.search(fr"^{val}\b", get):
                    get = re.sub(fr"^{val}(\W|$)", ' ', get)
                    get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
                    get = re.sub(r"(?<=2)(ND)|(?<=[4-9]|0)(TH|RTH)", '', get) #Strip any char of ordinal numbers
                    get = re.sub(r"(?<=[^1]3)(RD)", '', get); get = re.sub(r"(?<=11)(TH)", '', get)
        else:
            get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
            get = re.sub(r"(?<=2)(ND)|(?<=[4-9]|0)(TH|RTH)", '', get) #Strip any char of ordinal numbers
            get = re.sub(r"(?<=[^1]3)(RD)", '', get); get = re.sub(r"(?<=11)(TH)", '', get)
        for val in self.wordTypes: #Word Street Names
            if type(val) == dict:
                streA = '|'.join(val["ESPLANADE"])
                streB = '|'.join(val["BROADWAY"])
                grab = re.search(fr"(?!\d)?\W?({streA}|{streB})(\W|$)", get); wType = ''
                if grab:
                    wType = grab.group(1)
                    group1 = fr"(^\d+([- ]\d+)?)(?= ?[NSEW][. ] ?({wType})\.?(\W|$))"
                    group2 = fr"(^\d+([- ]\d+)?)(?= (NORTH |SOUTH |EAST |WEST )?({val})\.?(\W|$))"
                    group3 = r"(?=\d+([- ]\d+)? (AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$))^\d+([- ]\d+)?"
                    gANpat1 = re.search(fr"{group1}|{group2}", get)
                    gANpat2 = re.search(fr"{group3}", get)
                    if gANpat1:
                        new_addr_num = gANpat1.group().replace(' ', '-')
                    elif gANpat2:
                        new_addr_num = gANpat2.group().replace(' ', '-')
            else:
                group1 = fr"(^\d+([- ]\d+)?)(?= ?[NSEW][. ] ?({val})\.?(\W|$))"
                group2 = fr"(^\d+([- ]\d+)?)(?= (NORTH |SOUTH |EAST |WEST )?({val})\.?(\W|$))"
                group3 = r"(?=\d+([- ]\d+)? (AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$))^\d+([- ]\d+)?"
                gANpat1 = re.search(fr"{group1}|{group2}", get)
                gANpat2 = re.search(fr"{group3}", get)
                if gANpat1:
                    new_addr_num = gANpat1.group().replace(' ', '-')
                elif gANpat2:
                    new_addr_num = gANpat2.group().replace(' ', '-')
        for key, val in self.streetTypes.items(): #Regular Street Names
            sType = '|'.join(val)
            group = fr"(^\d+([- ]\d+)?)(?= ?[NSEW][. ]([A-Z]+ )+({sType})\.?(\W|$))"
            group1 = fr"(^\d+([- ]\d+)?)(?= ?[NSEW][. ]? ?\d+ ?({sType})\.?(\W|$))"
            group2 = fr"(^\d+([- ]\d+)?)(?=( ?(NORTH|SOUTH|EAST|WEST)? )((\w+\.? ?)+)({sType})\.?(\W|$))"
            group3 = r"(?=\d+([- ]\d+)? (AVENUE|AVEN\.?|AVE\.?|AV\.?|AE\.?) ([A-Z]|OF ([A-Z]+ )?[A-Z]+)(?=\W|$))^\d+([- ]\d+)?"
            gANpat1 = re.search(fr"{group}|{group1}|{group2}", get)
            gANpat2 = re.search(group3, get)
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
        get = (self.addr).upper(); new_street = ''; saintFlag = False #Uppercase and get street name to return
        if '/' in get:
            for key, val in self.states.items():
                if re.search(fr"\b{val}\b", get):
                    get = re.sub(fr"(^|\W){val}(\W|$)", ' ', get)
                    get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
                    get = re.sub(r"(?<=2)(ND)|(?<=[4-9]|0)(TH|RTH)", '', get) #Strip any char of ordinal numbers
                    get = re.sub(r"(?<=[^1]3)(RD)", '', get); get = re.sub(r"(?<=11)(TH)", '', get)
        else:
            get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
            get = re.sub(r"(?<=2)(ND)|(?<=[4-9]|0)(TH|RTH)", '', get) #Strip any char of ordinal numbers
            get = re.sub(r"(?<=[^1]3)(RD)", '', get); get = re.sub(r"(?<=11)(TH)", '', get)
        if re.search(r"(\W|^)(ST|SNT)\W", get): #Check for 'Saint'
            get1 = re.sub(r"(\W|^)(ST|SNT)\W", ' ', get)
            saintFlag = True
            new_street = self._search_cycle(get1, saintFlag)
            if new_street == "OTHER":
                saintFlag = False
                new_street = self._search_cycle(get, saintFlag)
        else:
            new_street = self._search_cycle(get, saintFlag)
        new_street = re.sub(r"^FT\W| FT\W", "FORT ", new_street) #Replace 'FT' with 'FORT'
        new_street = re.sub(r"(?<=1)ST", '', new_street) #Strip 1st ordinal number
        if re.search(r"\d+", new_street): #Apply ordinal numbers
            ordNum = self._ordinal_add(str(re.search(r"\d+", new_street).group()))
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
        gS = GeoLiberator(get).getStreet()
        gAN = GeoLiberator(get).getAddressNum()
        if self.__none_other(gS, gAN):
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

    def full_address(self, log=''):
        get = (self.addr).upper(); full_addr = '' #Uppercase and create 'full' address to return
        get = (re.sub(r"[\t!#$@%^*+=`~/]+| +", ' ', get)).strip(' ') #Strip any anomalies
        gA = GeoLiberator(get).getAddress()
        gST = GeoLiberator(get).get_state()
        gZP = GeoLiberator(get).get_zip()
        if self.__none_other(gA, gST, gZP):
            full_addr = gA + ', ' + gST + ' ' + gZP
        else:
            full_addr = "OTHER"

        if log != '': #Write to new or specfied file
            fileName = re.sub(r"\..+", '', log)
            if fileName.isdigit() or re.search(r'[\/:*?"<>|]', fileName):
                fileName = "newly_parsed_addresses"
            nf = open(f"{fileName}.txt", 'a')
            nf.write(full_addr + '\n')
            nf.close()
        return full_addr

#Count the lines in a file
def file_len(file_name):
    with open(file_name) as f:
        for i, L in enumerate(f):
            pass
    return i + 1

#Takes text file as input and parse argument to determine which address property to be standardized
def autoGeoLiberate(file_path: str, address_field='', parse="address", write=''):
    mode = True; lines = ''
    if not re.search(r"address|number|street", parse):
        raise ArgumentError(reason[0])
    if write != '':
        mode = False
    if address_field == '':
        if re.search(r".xlsx?$", file_path) or re.search(r".csv$", file_path):
            raise ArgumentError(reason[2])
        with open(file_path) as f:
            lines = f.readlines()
    else:
        if re.search(r".xlsx?$", file_path):
            df = pd.read_excel(file_path, usecols=[str(address_field)])
        elif re.search(r".csv$", file_path):
            df = pd.read_csv(file_path, usecols=[str(address_field)])
        else:
            raise ArgumentError(reason[1])
        lines = df[str(address_field)]
    if len(sys.argv) == 2 and write != '':
        if sys.argv[1] == '--status' or sys.argv[1] == "-S":
            FL = file_len(file_path)
            barIncr = int(FL * .025); barNum = 0; dashNum = 40; c = 0; lc = 0
            print('|' + ('-' * 40) + '|' + " [0.00%]", end=''); sys.stdout.flush()
            for line in lines:
                perc = (lc/FL)
                bar = '\r|' + ('█' * barNum) + ('-' * dashNum) + '|' + " [{:>.2%}]".format(perc)
                print(bar, end=''); sys.stdout.flush()
                c += 1; lc += 1
                if c == barIncr:
                    if barNum < 39:
                        c = 0; barNum += 1; dashNum -= 1
                        print(bar, end=''); sys.stdout.flush()
                elif lc == FL:
                    print('\r|' + ('█' * 40) + '|' + " [100%]  "); sys.stdout.flush()
                adr = GeoLiberator(str(line))
                if parse.lower() == "address":
                    adr.getAddress(log=write)
                elif parse.lower() == "number":
                    adr.getAddressNum(log=write)
                elif parse.lower() == "street":
                    adr.getStreet(log=write)
                elif parse.lower() == "state":
                    adr.get_state(log=write)
                elif parse.lower() == "zipcode":
                    out = adr.get_zip(log=write)
                elif parse.lower() == "full":
                    out = adr.full_address(log=write)
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
            elif parse.lower() == "state":
                out = adr.get_state(log=write)
            elif parse.lower() == "zipcode":
                out = adr.get_zip(log=write)
            elif parse.lower() == "full":
                out = adr.full_address(log=write)
            if mode == True:
                print(out)
        print("Done!")

#Takes address as input and parse argument to determine which address property to be standardized
def geoLiberate(addr: str, parse="address"):
    adr = GeoLiberator(str(addr))
    try:
        if parse.lower() == "address":
            out = adr.getAddress()
        elif parse.lower() == "number":
            out = adr.getAddressNum()
        elif parse.lower() == "street":
            out = adr.getStreet()
        elif parse.lower() == "state":
            out = adr.get_state()
        elif parse.lower() == "zipcode":
            out = adr.get_zip()
        elif parse.lower() == "full":
            out = adr.full_address()
        print(out)
    except (AttributeError, UnboundLocalError):
        raise ArgumentError(reason[0])

#Returns standardized address based on parse argument
def parse_address(addr: str, parse="address") -> str:
    adr = GeoLiberator(str(addr))
    try:
        if parse.lower() == "address":
            out = adr.getAddress()
        elif parse.lower() == "number":
            out = adr.getAddressNum()
        elif parse.lower() == "street":
            out = adr.getStreet()
        elif parse.lower() == "state":
            out = adr.get_state()
        elif parse.lower() == "zipcode":
            out = adr.get_zip()
        elif parse.lower() == "full":
            out = adr.full_address()
        return str(out)
    except (AttributeError, UnboundLocalError):
        raise ArgumentError(reason[0])
