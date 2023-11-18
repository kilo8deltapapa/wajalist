# Generate Worked All Japan Prefectures (WAJA) List from ADIF

This program generates a list of Japan Prefectures that have been confirmed, a list of unconfirmed prefectures, and a mapchartSave.txt file for upload to https://www.mapchart.net/japan.html to visualize the prefectures.

The following ADIF tags in the file being analyzied are used:
- \<STATION_CALLSIGN>  Your callsign; Optional, Needed for -c option
- \<STATE> Prefecture of station worked; Required
- \<DXCC> DXCC entity of station worked; Required
- \<MODE> Mode used; Optional, Needed for -m option
- \<BAND> Band used; Optional, Needed for -b option
- \<SAT_NAME> Name of satellite used; Optional, needed for -s option
- \<PROP_MODE> Propagation mode; Optional, needed for --satonly and --nosat options

This can be obtained by using the ARRL Logbook of the World Query by 
Rick Murphy K1MU found at URL: https://www.rickmurphy.net/lotwquery.htm

Information about JARL Worked All Japan Prefectures Award can be found here: https://www.jarl.org/English/4_Library/A-4-2_Awards/Award_Main.htm

## Requirements

- https://pypi.org/project/argparse/
- https://pypi.org/project/adif-io/

ja_prefectures.txt must be co-located in the same folder with the .exe or .py file.

## Installation


## Usage

usage: wajalist.py [-h] [-c CALL [CALL ...]] [-b BAND] [-m MODE] [-s SAT] [--satonly] [--nosat] filename

positional arguments:
  filename

options:
 - -h, --help            show this help message and exit
 - -c CALL [CALL ...], --call CALL [CALL ...]
                        list of callsigns, if not specified all callsigns are considered
 - -b BAND, --band BAND  band (eg. 20M, 2M, 70CM, etc...), if not specified all bands are considered
 - -m MODE, --mode MODE  mode (eg. CW, SSB, FT8, etc...), if not specified all modes are considered
 - -s SAT, --sat SAT     satellite name (eg. RS-44, IO-117, etc...), if not specified all satellites are included
 - --satonly             include only satellite QSOs
 - --nosat               exclude satellite QSOs


## Related Projects


## Credits


## License

[MIT](LICENSE) © [kilo8deltapapa](https://github.com/kilo8deltapapa).
