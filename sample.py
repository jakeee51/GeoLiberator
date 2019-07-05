from geoliberator import *

address = "123 N Main St"
#switch argument values:
#0 - Street Name
#1 - House Number
#2 - Full Address
geoLiberate(address, switch=0)

#getStreet()
#getAddressNum()
#getAddress()
lines = []
cmp = []
with open("sample.txt") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        GL_Object = GeoLiberator(line)
        cmp.append(GL_Object.getAddress())
for i in range(len(lines)):
    nlines = lines[i].strip('\n')
    print(f"{nlines} --> {cmp[i]}")

#Input File
#Output File
autoGeoLiberate(file_path="sample.txt", switch=2, write="write_to_file.txt")
