#!/usr/bin/env python3

# wajalist.py

"""
Description: This program generates a list of Japan Prefectures that have been
confirmed, a list of unconfirmed
prefectures, and a mapchartSave.txt file for upload to
https://www.mapchart.net/japan.html to visualize the prefectures.

The following ADIF tags in the file being analyzied are used:
<STATION_CALLSIGN>  Your callsign; Optional, Needed for -c option
<STATE> Prefecture of station worked; Required
<DXCC> DXCC entity of station worked; Required
<MODE> Mode used; Optional, Needed for -m option
<BAND> Band used; Optional, Needed for -b option
<SAT_NAME> Name of satellite used; Optional, needed for -s option
<PROP_MODE> Propagation mode; Optional, needed for --satonly and --nosat options

This can be obtained by using the ARRL Logbook of the World Query by
Rick Murphy K1MU found at URL: https://www.rickmurphy.net/lotwquery.htm

Author: Douglas C. Papay K8DP
Date Created: November 17, 2023
Date Modified: November 17, 2023
Version: 1.1
Python Version: 3.10.5
Dependencies: argparse,adif-io
License: MIT License
"""

import sys
import argparse
import adif_io

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument('filename')
parser.add_argument("-c", "--call", nargs='+', help = "list of callsigns, if \
    not specified all callsigns are considered")
parser.add_argument("-b", "--band", help = "band (eg. 20M, 2M, 70CM, \
    etc...), if not specified all bands are considered")
parser.add_argument("-m", "--mode", help = "mode (eg. CW, SSB, FT8, etc...), \
    if not specified all modes are considered")
parser.add_argument("-s", "--sat", help = "satellite name (eg. RS-44, IO-117, \
    etc...), if not specified all satellites are included")
parser.add_argument("--satonly", action='store_true', help = "include only \
    satellite QSOs")
parser.add_argument("--nosat", action='store_true', help = "exclude satellite \
    QSOs")

# Read arguments from command line
args = parser.parse_args()
if args.filename:
    input_filename = args.filename
else:
    sys.exit()

if args.call:
    callsign_list = args.call
    callsign_list = [x.upper() for x in callsign_list]
else:
    callsign_list = []

if args.band:
    BAND = args.band.upper()
else:
    BAND = ""

if args.mode:
    MODE = args.mode.upper()
else:
    MODE = ""

if args.sat:
    SAT = args.sat.upper()
else:
    SAT = ""

#Read prefecture list from file
pref_defs = []
with open("ja_prefectures.txt", "r", encoding="utf-8") as file2:
    while True:
        line = file2.readline().strip()
        if not line:
            break
        pref_defs.append(line.split(" "))

prefs_list = []
needed_list = []
qsocall_list = []

print("Worked All Japan Award (WAJA) Listing")

#read ADIF file into lists
qsos_raw, adif_header = adif_io.read_from_file(input_filename)

#look through qsos for those that match criteria
for qso in qsos_raw:

    station_callsign = qso["STATION_CALLSIGN"].upper()
    if station_callsign not in qsocall_list:
        qsocall_list.append(station_callsign)

    #not all records have sat_name
    try:
        SAT_NAME = qso["SAT_NAME"].upper()
    except KeyError as e:
        #key does not exist
        SAT_NAME = ""
    try:
        PROP_MODE = qso["PROP_MODE"]
    except KeyError as e:
        #key does not exist
        PROP_MODE = ""

    try:
        #read only records that are with Japan DXCC = 339
        #and conform to the specified band/mode/etc..
        if qso["DXCC"] == '339':
            if ((station_callsign in callsign_list) or len(callsign_list) == 0):
                if (SAT in (SAT_NAME, '') or not SAT):
                    if ((PROP_MODE == "SAT" and args.satonly) \
                    or (not args.satonly and not args.nosat) \
                    or (not PROP_MODE and args.nosat)):
                        if (MODE in (qso['MODE'], '') or not MODE):
                            if (BAND in (qso['BAND'], '') or not BAND):
                                if qso["STATE"] not in prefs_list:
                                    prefs_list.append(qso["STATE"])
    except KeyError as e:
        #other key does not exist
        pass

print("Callsigns in ADIF = ", ', '.join(qsocall_list),"\n")
print(len(qsos_raw), "records in ADIF\n")

#sort the prefecture list
prefs_list.sort()

for i in range(1,48):
    if not any(str(i).zfill(2) in sublist for sublist in prefs_list):
        needed_list.append(str(i).zfill(2))

print("Prefectures Confirmed:", len(prefs_list))
for p in prefs_list:
    print(pref_defs[int(p)-1][1], end=" ")
    print(p,end="\n")

print("\n")

print("Prefectures Needed:",len(pref_defs)-len(prefs_list))
for p in needed_list:
    print(pref_defs[int(p)-1][1], end=" ")
    print(p,end="\n")

print("\n")

if len(prefs_list) > 0:
    print("Generating mapchart.net file...")

    with open("mapchartSave-ja.txt", "w", encoding="utf-8") as f:
        print('{"groups":{"#e0ecf4":{"label":"Confirmed LoTW","paths":[', end="", file=f)

        for i,p in enumerate(prefs_list):
            if i < len(prefs_list) - 1:
                print('"' + pref_defs[int(p)-1][1] + '"',end=",", file=f)
            else:
                print('"' + pref_defs[int(p)-1][1] + '"',end="", file=f)

        print(']},"#cc3333":{"label":"Needed","paths":[',end="", file=f)

        for i,p in enumerate(needed_list):
            if i < len(needed_list) - 1:
                print('"' + pref_defs[int(p)-1][1] + '"',end=",", file=f)
            else:
                print('"' + pref_defs[int(p)-1][1] + '"', file=f)

        print(']}},"title":"' + ', '.join(callsign_list) + 'Worked All Japan \
        Prefectures","hidden":[],"background":"#fff","borders":"#000",\
        "legendFont":"Helvetica","legendFontColor":"#000",\
        "legendBgColor":"#00000000","legendWidth":150,"areBordersShown":true,\
        "defaultColor":"#d1dbdd","labelsColor":"#6a0707",\
        "strokeWidth":"medium","areLabelsShown":true,\
        "legendPosition":"top_left","legendSize":"medium",\
        "legendStatus":"show","scalingPatterns":true,\
        "legendRowsSameColor":true,"legendColumnCount":2}', file=f)

    print("   Done.\n")
    print("File can be uploaded to https://www.mapchart.net/japan.html for map display.\n")
else:
    print("No prefectures confirmed, mapchart.net file was not created!")
