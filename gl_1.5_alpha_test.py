from geoliberator import *
import pandas as pd
import time
t0 = time.process_time()
mSet = True

anon_street_trials = ['22E100ST', '123 N. 52 ST.', '123 N.52 STR', '123 N 52STRE',
               '123 N52ST.', '123 N 52 STREET', '123 N MAIN STREET', '123 52ST.',
               '123 52 STR', '123 STANLEY STRE', '123 NORTH MAIN STREET,', '123 RTH 52 STREET',
               '123 NORTH MAIN STREET', '123-4 MARTIN LUTHER KING JR ST.', '100 ST', '100 STREET',
               '100ST', '100 AV', 'EAST 100 ST', 'CHARLES ST',
               'EAST CHARLES ST', 'E 100 ST', 'E100ST', 'E 100ST',
               'E100 ST', 'E. 100ST']
checker_anon = ['EAST 100th STREET', 'NORTH 52nd STREET', 'NORTH 52nd STREET', 'NORTH 52nd STREET',
                'NORTH 52nd STREET', 'NORTH 52nd STREET', 'NORTH MAIN STREET', '52nd STREET',
                '52nd STREET', 'STANLEY STREET', 'NORTH MAIN STREET', '52nd STREET',
                'NORTH MAIN STREET', 'MARTIN LUTHER KING JR STREET', '100th STREET', '100th STREET',
                '100th STREET', '100th AVENUE', 'EAST 100th STREET', 'CHARLES STREET',
                'EAST CHARLES STREET', 'EAST 100th STREET', 'EAST 100th STREET', 'EAST 100th STREET',
                'EAST 100th STREET', 'EAST 100th STREET']
cardinal_trials = ['123 N. 52nd ST', '123 N52 STR', '123 N 52STRE',
                  '123 N52ST', '123 N 52 STREET', '123 N MAIN STREET']
nc_trials = ['123 52ST', '123 52 STR', '123 MAIN STRE',
             '123 NORTH 52 STREET', '123 NORTH MAIN STREET', '123 MARTIN LUTHER KING JR ST']
ordinal_trials = ['6-6 6TH AVE PREK, MANHATTAN 11220', '122-52 MULBERRY STRE COMF, NEW YORK 10013',
                  '1 MURRAY HULBERT AVE, STATEN ISLAND 10305', '13 NELSON ST ITS-NMANH DOT, BROOKLYN 11231',
                  '1234 11th AVE', '1234-02 NORTH 3rd ST']
checker_street = ['NORTH 52nd STREET', 'NORTH 52nd STREET', 'NORTH 52nd STREET',
                  'NORTH 52nd STREET', 'NORTH 52nd STREET', 'NORTH MAIN STREET',
                  '52nd STREET', '52nd STREET', 'MAIN STREET',
                  'NORTH 52nd STREET', 'NORTH MAIN STREET', 'MARTIN LUTHER KING JR STREET',
                  '6th AVENUE', 'MULBERRY STREET', 'MURRAY HULBERT AVENUE',
                  'NELSON STREET', '11th AVENUE', 'NORTH 3rd STREET']
checker_num = ['123', '123', '123', '123', '123', '123',
               '123', '123', '123', '123', '123', '123',
               '6-6', '122-52', '1', '13', '1234', '1234-02']
checker_address = ['123 NORTH 52nd STREET', '123 NORTH 52nd STREET', '123 NORTH 52nd STREET', '123 NORTH 52nd STREET',
                   '123 NORTH 52nd STREET', '123 NORTH MAIN STREET', '123 52nd STREET', '123 52nd STREET',
                   '123 MAIN STREET', '123 NORTH 52nd STREET', '123 NORTH MAIN STREET',
                   '123 MARTIN LUTHER KING JR STREET', '6-6 6th AVENUE', '122-52 MULBERRY STREET',
                   '1 MURRAY HULBERT AVENUE', '13 NELSON STREET', '1234 11th AVENUE', '1234-02 NORTH 3rd STREET']

def mergeMatch():
    n1 = open("merged_addresses.txt", 'w')
    n2 = open("merged_address_nums.txt", 'w')
    n3 = open("merged_streets.txt", 'w')
    data = pd.read_excel("GL_Staging.xlsx")
    for i in data.index:
        if data["addr1"][i] != "OTHER" and data["addr2"][i] != "OTHER":
            n1.write(data["addr1"][i] + '\n')
        elif data["addr1"][i] != "OTHER" and data["addr2"][i] == "OTHER":
            n1.write(data["addr1"][i] + '\n')
        elif data["addr2"][i] != "OTHER" and data["addr1"][i] == "OTHER":
            n1.write(data["addr2"][i] + '\n')
        else:
            n1.write("OTHER\n")
    for i in data.index:
        if data["addrNum1"][i] != "OTHER" and data["addrNum2"][i] != "OTHER":
            n2.write(str(data["addrNum1"][i]) + '\n')
        elif data["addrNum1"][i] != "OTHER" and data["addrNum2"][i] == "OTHER":
            n2.write(str(data["addrNum1"][i]) + '\n')
        elif data["addrNum2"][i] != "OTHER" and data["addrNum1"][i] == "OTHER":
            n2.write(str(data["addrNum2"][i]) + '\n')
        else:
            n2.write("OTHER\n")
    for i in data.index:
        if data["street1"][i] != "OTHER" and data["street2"][i] != "OTHER":
            n3.write(data["street2"][i] + '\n')
        elif data["street1"][i] != "OTHER" and data["street2"][i] == "OTHER":
            n3.write(data["street1"][i] + '\n')
        elif data["street2"][i] != "OTHER" and data["street1"][i] == "OTHER":
            n3.write(data["street2"][i] + '\n')
        else:
            n3.write("OTHER\n")
    n1.close(); n2.close(); n3.close()

def basicTest():
    catcher = []
    catcher1 = []
    catcher2 = []
    catcher3 = []
    for addr in anon_street_trials:
        adr = GeoLiberator(addr)
        catcher.append(adr.getStreet(mode=mSet))
    for addr in cardinal_trials:
        adr = GeoLiberator(addr)
        catcher1.append(adr.getStreet(mode=mSet))
    for addr in nc_trials:
        adr = GeoLiberator(addr)
        catcher1.append(adr.getStreet(mode=mSet))
    for addr in ordinal_trials:
        adr = GeoLiberator(addr)
        catcher1.append(adr.getStreet(mode=mSet))
    c = 0; gg = 0; C = 0; ggg = 0
    for i in checker_street:
        if i == catcher1[c]:
            gg += 1
        c += 1
    for i in checker_anon:
        if i == catcher[C]:
            ggg += 1
        C += 1
    if gg == 18 and ggg == 26:
        print("\n*ALL Street Name Trials Successful!*\n")
    print("________________________________\n\n")
    for addr in cardinal_trials:
        adr = GeoLiberator(addr)
        catcher2.append(adr.getAddressNum(mode=mSet))
    for addr in nc_trials:
        adr = GeoLiberator(addr)
        catcher2.append(adr.getAddressNum(mode=mSet))
    for addr in ordinal_trials:
        adr = GeoLiberator(addr)
        catcher2.append(adr.getAddressNum(mode=mSet))
    c = 0; gg = 0
    for i in checker_num:
        if i == catcher2[c]:
            gg += 1
        c += 1
    if gg == 18:
        print("\n*ALL Address Number Trials Successful!*\n")
    print("________________________________\n\n")
    for addr in cardinal_trials:
        adr = GeoLiberator(addr)
        catcher3.append(adr.getAddress(mode=mSet))
    for addr in nc_trials:
        adr = GeoLiberator(addr)
        catcher3.append(adr.getAddress(mode=mSet))
    for addr in ordinal_trials:
        adr = GeoLiberator(addr)
        catcher3.append(adr.getAddress(mode=mSet))
    c = 0; gg = 0
    for i in checker_address:
        if i == catcher3[c]:
            gg += 1
        c += 1
    if gg == 18:
        print("\n*ALL Address Trials Successful!*\n")

##GeoLiberator("123 MAIN STREET, WHITLE PLAINS 10601").getStreet(mode=mSet)
##GeoLiberator("123 CONCOURSE & COOPER STREET, MANHATTAN 11220").getStreet(mode=mSet)
##GeoLiberator("123-4 LEXINGTON AVENUE").getStreet(mode=mSet)
##GeoLiberator("W 114 ST FA").getStreet(mode=mSet)
##GeoLiberator("199 WATER ST 18 FL").getStreet(mode=mSet)
##GeoLiberator("123 ST NICK AVE").getStreet(mode=mSet)
##GeoLiberator("321 MAIN STREET, MANHATTAN 11220").getAddressNum(mode=mSet)
##GeoLiberator("321 4 4th STREET, MANHATTAN 11220").getAddressNum(mode=mSet)
##GeoLiberator("432-1 STANLEY STREET, MANHATTAN 11220").getAddressNum(mode=mSet)
##GeoLiberator("%%%321 MAIN STREET, MANHATTAN 11220").getAddress(mode=mSet)
##GeoLiberator("@ 321 STREET, MANHATTAN 11220").getAddress(mode=mSet)
##GeoLiberator("432-1 STANLEY STREET, MANHATTAN 11220").getAddress(mode=mSet)

##mergeMatch()
##autoGeoLiberate("hold.txt", 2)
basicTest()

t1 = time.process_time()
total = t1 - t0
if __name__ == "__main__":
    print(f"Timestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
    print("Module Time Elapsed:", total, "seconds")
