from geoliberator import *
import time
t0 = time.process_time()
mSet = True

##data = pd.read_excel("NYEM_Staging.xlsx")
##for i in data.index:
##    if data["addr1"][i] != "OTHER" and data["addr2"][i] != "OTHER":
##        if data["addr1"][i] == data["addr2"][i]:
##            print(data["addr1"][i])
##        else:
##            print("DIFFER")
##    elif data["addr1"][i] != "OTHER" and data["addr2"][i] == "OTHER":
##        print(data["addr1"][i])
##    elif data["addr2"][i] != "OTHER" and data["addr1"][i] == "OTHER":
##        print(data["addr2"][i])
##    else:
##        print("OTHER")

##with open("hold.txt") as f:
##    lines = f.readlines()
##    for line in lines:
##        adr = GeoLiberator(str(line))
##        adr.getAddress(mode=mSet)

##cardinal_trials = ['123 N 52 ST', '123 N52 STR', '123 N 52STRE',
##                  '123 N52ST', '123 N 52 STREET', '123 N MAIN STREET']
##nc_trials = ['123 52ST', '123 52 STR', '123 MAIN STRE',
##    '123 NORTH 52 STREET', '123 NORTH MAIN STREET', '123 MARTIN LUTHER KING JR ST']
##ordinal_trials = ['6-6 6TH AVE PREK, MANHATTAN 11220', '122-52 MULBERRY STRE COMF, NEW YORK 10013',
##                  '1 MURRAY HULBERT AVE, STATEN ISLAND 10305', '13 NELSON ST ITS-NMANH DOT, BROOKLYN 11231',
##                  '1234 4th AVE', '1234-02 NORTH 3rd ST']
##checker_street = ['NORTH 52 STREET', 'NORTH 52 STREET', 'NORTH 52 STREET',
##           'NORTH 52 STREET', 'NORTH 52 STREET', 'NORTH MAIN STREET',
##           '52 STREET', '52 STREET', 'MAIN STREET',
##           'NORTH 52 STREET', 'NORTH MAIN STREET', 'MARTIN LUTHER KING JR STREET',
##           '6 AVENUE', 'MULBERRY STREET', 'MURRAY HULBERT AVENUE',
##           'NELSON STREET', '4 AVENUE', 'NORTH 3 STREET']
##checker_num = ['123', '123', '123', '123', '123', '123',
##               '123', '123', '123', '123', '123', '123',
##               '6-6', '122-52', '1', '13', '1234', '1234-02']
##catcher1 = []
##catcher2 = []
##catcher3 = []
##
##for addr in cardinal_trials:
##    adr = GeoLiberator(addr)
##    catcher1.append(adr.getStreet(mode=mSet))
##for addr in nc_trials:
##    adr = GeoLiberator(addr)
##    catcher1.append(adr.getStreet(mode=mSet))
##for addr in ordinal_trials:
##    adr = GeoLiberator(addr)
##    catcher1.append(adr.getStreet(mode=mSet))
##c = 0; gg = 0
##for i in checker_street:
##    if i == catcher1[c]:
##        gg += 1
##    c += 1
##if gg == 18:
##    print("\n*ALL Street Name Trials Successful!*\n")
##print("________________________________\n\n")
##for addr in cardinal_trials:
##    adr = GeoLiberator(addr)
##    catcher2.append(adr.getAddressNum(mode=mSet))
##for addr in nc_trials:
##    adr = GeoLiberator(addr)
##    catcher2.append(adr.getAddressNum(mode=mSet))
##for addr in ordinal_trials:
##    adr = GeoLiberator(addr)
##    catcher2.append(adr.getAddressNum(mode=mSet))
##c = 0; gg = 0
##for i in checker_num:
##    if i == catcher2[c]:
##        gg += 1
##    c += 1
##if gg == 18:
##    print("\n*ALL Address Number Trials Successful!*\n")
##print("________________________________\n\n")
##for addr in cardinal_trials:
##    adr = GeoLiberator(addr)
##    catcher3.append(adr.getAddress(mode=mSet))
##for addr in nc_trials:
##    adr = GeoLiberator(addr)
##    catcher3.append(adr.getAddress(mode=mSet))
##for addr in ordinal_trials:
##    adr = GeoLiberator(addr)
##    catcher3.append(adr.getAddress(mode=mSet))
##c = 0; gg = 0
##for i in checker_street:
##    if i == catcher1[c]:
##        gg += 1
##    c += 1
##if gg == 18:
##    print("\n*ALL Address Trials Successful!*\n")

##GeoLiberator("123 MAIN STREET, WHITLE PLAINS 10601").getStreet(mode=mSet)
##GeoLiberator("123 CONCOURSE & COOPER STREET, MANHATTAN 11220").getStreet(mode=mSet)
##GeoLiberator("123-4 LEXINGTON AVENUE").getStreet(mode=mSet)
##GeoLiberator("321 MAIN STREET, MANHATTAN 11220").getAddressNum(mode=mSet)
##GeoLiberator("321 STREET, MANHATTAN 11220").getAddressNum(mode=mSet)
##GeoLiberator("432-1 STANLEY STREET, MANHATTAN 11220").getAddressNum(mode=mSet)
##GeoLiberator("%%%321 MAIN STREET, MANHATTAN 11220").getAddress(mode=mSet)
##GeoLiberator("@ 321 STREET, MANHATTAN 11220").getAddress(mode=mSet)
##GeoLiberator("432-1 STANLEY STREET, MANHATTAN 11220").getAddress(mode=mSet)

t1 = time.process_time()
total = t1 - t0
if __name__ == "__main__":
    print(f"Timestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
    print("Module Time Elapsed:", total, "seconds")
