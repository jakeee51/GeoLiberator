<a href="https://pypi.org/project/GeoLiberator">
  <img src="https://img.shields.io/pypi/v/geoliberator.svg" alt="latest release" />
</a>

<a href="https://pepy.tech/project/geoliberator">
  <img src="https://static.pepy.tech/badge/geoliberator" alt="downloads" />
</a>

<a href="https://travis-ci.org/github/jakeee51/GeoLiberator">
  <img src="https://travis-ci.org/jakeee51/GeoLiberator.svg?branch=master&status=passed" />
</a>

# The-GeoLiberator-Python-Module

This module is an address parser. It takes in an address as an argument and outputs a standardized version. Otherwise, 'OTHER' will be the result if the parser fails.
"It is alike a liberal because it takes in any variant addresses indiscriminately.
And it is a liberator because it liberates the addresses from their inconsistencies."
*(Note: This module does not do address validation but it will parse any address you throw at it to the best of its ability. Especially NYC addresses.)*

<h2><b>Usage:</b></h2>

To start, import with your desired handle to call upon the module with ease. The function `parse_address()` returns the value while `geoLiberate()` prints the value.
```python
import GeoLiberator as GL

GL.parse_address("123 Example St, NY 01234", "address") # 'address' to parse the address
# Returns: '123 EXAMPLE STREET'

GL.geoLiberate("123 Example St, NY 01234", "full") # 'full' to parse the full address
# Prints: 123 EXAMPLE STREET, NEW YORK 01234

GL.geoLiberate("123 Example St, NY 01234", "number") # 'number' to parse the address house number
# Prints: 123

GL.geoLiberate("123 Example St, NY 01234", "street") # 'street' to parse the street name
# Prints: EXAMPLE STREET
```
The first argument is any address of data type string.

The second argument, 'parse', as you may have noticed, determines what gets parsed. *(Note: if no argument given, parses address by default)*
* "address" - Address (only)
* "full" - Full Address (including state and zipcode)
* "number" - House Number
* "street" - Street Name
* "state" - State
* "zipcode" - Zipcode

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
BOB ROAD
NORTH JOHNSON AVENUE
2nd STREET
```
For that really lengthy list of addresses in a file, it's reccommended to use autoGeoLiberate() in your program and run it in a cli with the flag `--status`(`-S` for short) to monitor the module's progress. Like so:

`python my_program.py --status`


<h2><b><i>For developmental purposes:</i></b></h2>

```python
address_object = GL.GeoLiberator("123 Example St") # Create a 'GeoLiberator Object' with address as an argument
#This new address object can then be parsed using the dot operator like so:
address_object.full_address() # includes state and zipcode
address_object.getAddress()
address_object.getAddressNum()
address_object.getStreet()
```
These member functions return a string value.

**Member Function Parameters:**
```python
getAddress(log = '')
```
The 'log' parameter is for entering in a file name to _append_ all address results to a log file.
*(Note: these functions will always return a value)*

# Copyright
Copyright (c) 2020 The Python Packaging Authority. Released under the MIT License.
