import sys
import re
import argparse
import adif_io

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument('filename')
parser.add_argument("-c", "--call", help = "callsign, if not specified all callsigns are considered")
parser.add_argument("-b", "--band", help = "band (eg. 20M, 2M, 70CM, etc...), if not specified all bands are considered")
parser.add_argument("-m", "--mode", help = "mode (eg. CW, SSB, FT8, etc...), if not specified all modes are considered")

# Read arguments from command line
args = parser.parse_args()
if args.filename:
    input_filename = args.filename
else:
    quit()
    
if args.call:
    callsign = args.call
else:    
    callsign = ""

if args.band:
    band = args.band
else:    
    band = ""
    
if args.mode:
    mode = args.mode
else:    
    mode = ""    
    
#Read prefecture list from file
pref_defs = []
with open("ja_prefectures.txt", "r") as file2:
    while True:
        line = file2.readline().strip()
        if not line:
            break
        else:
            pref_defs.append(line.split(" "))

prefs_list = []
needed_list = []

#read ADIF file into lists
qsos_raw, adif_header = adif_io.read_from_file(input_filename)

#look through qsos for those that match criteria
for qso in qsos_raw:
    try:
        # read only records that are with Japan DXCC = 339
        if qso["DXCC"] == '339' \
            and (qso["STATION_CALLSIGN"] == callsign.upper() or callsign == "") \
            and (qso["MODE"] == mode.upper() or mode == "") \
            and (qso["BAND"] == band.upper() or band == ""):
            if qso["STATE"] not in prefs_list:
                prefs_list.append(qso["STATE"])                
    except:
        pass
        
#sort the prefecture list
prefs_list.sort()

for i in range(1,48):
    if not any(str(i).zfill(2) in sublist for sublist in prefs_list):
        needed_list.append(str(i).zfill(2))

print("Prefectures Confirmed:", len(prefs_list))
for p in prefs_list:
    print(pref_defs[int(p)-1][1])
print("\n")
print("Prefectures Needed:",47-len(prefs_list))

for p in needed_list:
    print(pref_defs[int(p)-1][1])

print("\n")
print("Generating mapchart.net file...")


with open("mapchartSave.txt", "w") as f:
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
    if callsign != "":
        callsign = callsign + ' - '
    print(']}},"title":"'+ callsign +'Worked All Japan Prefectures","hidden":[],"background":"#fff","borders":"#000","legendFont":"Helvetica","legendFontColor":"#000","legendBgColor":"#00000000","legendWidth":150,"areBordersShown":true,"defaultColor":"#d1dbdd","labelsColor":"#6a0707","strokeWidth":"medium","areLabelsShown":true,"legendPosition":"top_left","legendSize":"medium","legendStatus":"show","scalingPatterns":true,"legendRowsSameColor":true,"legendColumnCount":2}', file=f)

print("   Done.\n")
print("File can be uploaded to https://www.mapchart.net/japan.html for map display.\n")