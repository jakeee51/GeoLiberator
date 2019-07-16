# The-GeoLiberator-Python-Module
This module is an address parser. It takes in an address as an argument and outputs a standardized version. Otherwise, 'OTHER' will be the result if the parser fails.
"It is alike a liberal because it takes in any variant addresses indiscriminately.
And it is a liberator because it liberates the addresses from their inconsistencies."
*(Note: This module does not do address validation but it will parse any address you throw at it to the best of its ability)*

**Usage:**

To start, import with your desired handle to call upon the module with ease,
```python
import GeoLiberator as GL

GL.geoLiberate("123 Example St", "address") # 'address' to parse the full address
#Output: 123 EXAMPLE STREET

GL.geoLiberate("123 Example St", "number") # 'number' to parse the address house number
#Output: 123

GL.geoLiberate("123 Example St", "street") # 'street' to parse the full street
#Output: EXAMPLE STREET
```
The first argument is any address of data type string.

The second argument, as you may have noticed, determines what gets parsed. *(Note: if no agument given, parses address by default)*
* "address" - Full Address
* "number" - House Number
* "street" - Full Street

The following function's first argument is a file containing a list of addresses. It automatically loops through the rows and parses each address.
```python
GL.autoGeoLiberate("file.txt", "street", "output_file_name.txt") # 'street' to parse full street name
#If no output file name given, program will print all parsed addresses
```

Let's say 'file.txt' contains the following:
```
123 Bob Rd
321 N Johnson Aven
123-4 2nd St
```
Output would look like this:
```
123 BOB ROAD
321 NORTH JOHNSON AVENUE
123-4 2nd STREET
```
For that really lengthy list of addresses in a file, it's reccommended to use autoGeoLiberate() in your program and run it in a cli with the flag `--status`(`-S` for short) to monitor the module's progress. Like so: `python my_progam.py --status`

***For developmental purposes:***

```python
address_object = GL.GeoLiberator("123 Example St") # Create a 'GeoLiberator Object' with address as an argument
#This new address object can then be parsed using the dot operator like so:
address_object.getAddress()
address_object.getAddressNum()
address_object.getStreet()
```
These member functions return a string value.

**Function Parameters:**
```python
getAddress(log = '')
```
The 'log' parameter is for entering in a file name to _append_ all address results to a log file.
*(Note: these functions will always return a value)*

# Copyright
Copyright (c) 2019 The Python Packaging Authority. Released under the MIT License.
